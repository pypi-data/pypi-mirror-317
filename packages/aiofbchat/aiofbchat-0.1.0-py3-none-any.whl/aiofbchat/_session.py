from attrs import define, field
import datetime
import aiohttp
import random
import re
import urllib.request
from yarl import URL
from http.cookies import SimpleCookie, BaseCookie

# TODO: Only import when required
# Or maybe just replace usage with `html.parser`?

from ._common import log, req_log, kw_only
from . import _graphql, _util, _exception

from typing import Optional, Mapping, Dict, List, NamedTuple

try:
    from aiohttp_socks import ProxyType, ProxyConnector, ProxyTimeoutError
except ImportError:
    ProxyType = None
    ProxyConnector = None


    class ProxyTimeoutError(Exception):
        pass

def parse_kv(vals: List[str]) -> Dict[str, str]:
    kv = {}
    for val in vals:
        split = val.strip().split("=", 1)
        if len(split) == 1:
            kv[split[0]] = True
        else:
            kv[split[0]] = split[1]
    return kv


class AltSvc(NamedTuple):
    alt_authority: str
    max_age: int
    persist: bool
    extra_meta: Dict[str, str]


def parse_alt_svc(r: aiohttp.ClientResponse) -> Dict[str, AltSvc]:
    try:
        header = r.headers["Alt-Svc"]
    except KeyError:
        return {}
    if header.lower() == "clear":
        return {}
    services = {}
    for service in header.split(","):
        vals = service.split(";")
        try:
            protocol_id, alt_authority = vals[0].split("=")
        except ValueError:
            continue
        alt_authority: str = alt_authority.strip('"')
        kv = parse_kv(vals[1:])
        try:
            max_age = int(kv.pop("max_age"))
        except (KeyError, ValueError):
            max_age = 86400
        try:
            persist = kv.pop("persist") == "1"
        except KeyError:
            persist = False
        services[protocol_id] = AltSvc(alt_authority, max_age, persist, extra_meta=kv)
    return services


def base36encode(number: int) -> str:
    """Convert from Base10 to Base36."""
    # Taken from https://en.wikipedia.org/wiki/Base36#Python_implementation
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"

    sign = "-" if number < 0 else ""
    number = abs(number)
    result = ""

    while number > 0:
        number, remainder = divmod(number, 36)
        result = chars[remainder] + result

    return sign + result


def generate_message_id(now: datetime.datetime, client_id: str) -> str:
    k = _util.datetime_to_millis(now)
    l = int(random.random() * 4294967295)
    return "<{}:{}-{}@mail.projektitan.com>".format(k, l, client_id)


def get_user_id(domain: str, session: aiohttp.ClientSession) -> str:
    try:
        rtn = session.cookie_jar.filter_cookies(URL(f"https://{domain}")).get("c_user")
    except (AttributeError, KeyError):
        raise AttributeError("Could not find user id from cookies")
    if rtn is None:
        raise _exception.ParseError("Could not find user id from cookies. Cookie is None")
    return rtn if isinstance(rtn, str) else str(rtn.value)


def session_factory(user_agent: Optional[str] = None) -> aiohttp.ClientSession:
    connector = None
    try:
        http_proxy = urllib.request.getproxies()["http"]
    except KeyError:
        pass
    else:
        if ProxyConnector:
            connector = ProxyConnector.from_url(http_proxy)
        else:
            log.warning("http_proxy is set, but aiohttp-socks is not installed")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://www.facebook.com/",
        "Host": "www.facebook.com",
        "Origin": "https://www.facebook.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Connection": "keep-alive",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip", #, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
    return aiohttp.ClientSession(connector=connector, headers=headers)


def login_cookies(at: datetime.datetime):
    return {"act": "{}/0".format(_util.datetime_to_millis(at))}


def client_id_factory() -> str:
    return hex(int(random.random() * 2 ** 31))[2:]


def prefix_url(domain: str, path: str) -> URL:
    if path.startswith("/"):
        return URL(f"https://www.{domain}" + path)
    return URL(path)


@define(slots=True, kw_only=kw_only, repr=False, eq=False, auto_attribs=True)
class Session:
    """Stores and manages state required for most Facebook requests.

    This is the main class, which is used to login to Facebook.
    """

    _user_id: str
    _fb_dtsg: str
    _revision: int
    domain: str
    _onion: Optional[str] = None
    _session: aiohttp.ClientSession = field(factory=session_factory)
    _counter: int = 0
    _client_id: str = field(factory=client_id_factory)

    def _prefix_url(self, path: str) -> URL:
        return prefix_url(self.domain, path)

    @property
    def user(self):
        """The logged in user."""
        from . import _threads

        # TODO: Consider caching the result

        return _threads.User(session=self, id=self._user_id)

    def __repr__(self) -> str:
        # An alternative repr, to illustrate that you can't create the class directly
        return "<fbchat.Session user_id={}>".format(self._user_id)

    def _get_params(self):
        self._counter += 1
        return {
            "__a": 1,
            "__req": base36encode(self._counter),
            "__rev": self._revision,
            "fb_dtsg": self._fb_dtsg,
        }

    async def is_logged_in(self) -> bool:
        """Send a request to Facebook to check the login status.

        Returns:
            Whether the user is still logged in

        Example:
            >>> assert session.is_logged_in()
        """
        # Send a request to the login url, to see if we're directed to the home page
        try:
            r = await self._session.get(self._prefix_url("/login/"), allow_redirects=False)
        except aiohttp.ClientError as e:
            _exception.handle_requests_error(e)
            raise Exception("handle_requests_error did not raise exception")
        _exception.handle_http_error(r.status)
        location = r.headers.get("Location")
        return location in (f"https://www.{self.domain}/",
                            # We include this as a "logged in" status, since the user is logged in,
                            # but needs to verify the session elsewhere
                            f"https://www.{self.domain}/checkpoint/block/")

    @classmethod
    async def _from_session(cls, session: aiohttp.ClientSession, domain: str
                            ) -> Optional['Session']:
        # TODO: Automatically set user_id when the cookie changes in the session
        user_id = get_user_id(domain, session)

        # Make a request to the main page to retrieve ServerJSDefine entries
        try:
            r = await session.get(prefix_url(domain, "/"), allow_redirects=True, headers={
                "Accept": "text/html",
            })
        except aiohttp.ClientError as e:
            _exception.handle_requests_error(e)
            raise Exception("handle_requests_error did not raise exception")
        _exception.handle_http_error(r.status)

        html = await r.text()
        if len(html) == 0:
            raise _exception.FacebookError("Got empty response when trying to check login")


        fb_dtsg = re.search(r'"DTSGInitialData".*?"token":"(.*?)"', html)
        if fb_dtsg:
            fb_dtsg = fb_dtsg.group(1)
        if not fb_dtsg:
            # Happens when the client is not actually logged in
            raise _exception.NotLoggedIn(
                "Found empty fb_dtsg, the session was probably invalid."
            )
        try:
            revision = re.search(r'client_revision":(\d+)', html)
            if revision:
                revision = revision.group(1)
        except TypeError:
            raise TypeError("Couldnt find revision id")
        onion = None
        alt_svc_data = parse_alt_svc(r)
        if "h2" in alt_svc_data and alt_svc_data["h2"].alt_authority.endswith(".onion:443"):
            # TODO remember expiry too?
            onion = alt_svc_data["h2"].alt_authority
            log.info("Got onion alt-svc %s", onion)

        return cls(user_id=user_id, fb_dtsg=fb_dtsg, revision=revision, session=session, domain=domain, onion=onion)

    def get_cookies(self) -> Optional[Mapping[str, str]]:
        """Retrieve session cookies, that can later be used in `from_cookies`.

        Returns:
            A dictionary containing session cookies

        Example:
            >>> cookies = session.get_cookies()
        """
        cookie = self._session.cookie_jar.filter_cookies(URL(f"https://{self.domain}"))
        return {key: morsel.value for key, morsel in cookie.items()}

    @classmethod
    async def from_cookies(cls, cookies: Mapping[str, str], user_agent: Optional[str] = None, domain: str = "messenger.com") -> 'Session':
        """Load a session from session cookies.

        Args:
            cookies: A dictionary containing session cookies

        Example:
            >>> cookies = session.get_cookies()
            >>> # Store cookies somewhere, and then subsequently
            >>> session = fbchat.Session.from_cookies(cookies)
        """
        session = session_factory(user_agent=user_agent)

        if isinstance(cookies, BaseCookie):
            cookie = cookies
        else:
            cookie = SimpleCookie()
            for key, value in cookies.items():
                cookie[key] = value
                cookie[key].update({"domain": domain, "path": "/"})
        session.cookie_jar.update_cookies(cookie, URL(f"https://{domain}"))

        return await cls._from_session(session=session, domain=domain)

    async def _post(self, url, data, files=None, as_graphql=False):
        data.update(self._get_params())
        if files:
            payload = aiohttp.FormData()
            for key, value in data.items():
                payload.add_field(key, str(value))
            for key, (name, file, content_type) in files.items():
                payload.add_field(key, file, filename=name, content_type=content_type)
            data = payload
        real_url = self._prefix_url(url)
        kwargs = {}
        if self._onion:
            # TODO is there some way to change the host aiohttp connects to without changing the
            #      domain it uses for TLS, cookies and the Host header?
            kwargs["ssl"] = False
            kwargs["headers"] = {"Host": real_url.host}
            kwargs["cookies"] = self._session.cookie_jar.filter_cookies(real_url)
            real_url = real_url.with_host(real_url.host.replace(self.domain, self._onion))
        attempt = 1
        while True:
            try:
                r = await self._session.post(real_url, data=data, **kwargs)
                break
            except aiohttp.ClientError as e:
                _exception.handle_requests_error(e)
                raise Exception("handle_requests_error did not raise exception")
            except ProxyTimeoutError:
                if attempt >= 3:
                    raise
                log.warning("Got ProxyTimeoutError, retrying...")
                attempt += 1
        _exception.handle_http_error(r.status)
        text = await r.text()
        if text is None or len(text) == 0:
            raise _exception.HTTPError("Error when sending request: Got empty response")
        if as_graphql:
            return _graphql.response_to_json(text)
        else:
            text = _util.strip_json_cruft(text)
            j = _util.parse_json(text)
            log.debug(j)
            return j

    async def _payload_post(self, url, data, files=None):
        if files:
            req_log.debug("POST %s %s with %d files", url, data, len(files))
        else:
            req_log.debug("POST %s %s", url, data)
        j = await self._post(url, data, files=files)
        _exception.handle_payload_error(j)

        # update fb_dtsg token if received in response
        if "jsmods" in j:
            define = _util.get_jsmods_define(j["jsmods"]["define"])
            fb_dtsg = get_fb_dtsg(define)
            if fb_dtsg:
                self._fb_dtsg = fb_dtsg

        try:
            return j["payload"]
        except (KeyError, TypeError) as e:
            raise _exception.ParseError("Missing payload", data=j) from e

    async def _graphql_requests(self, *queries):
        # TODO: Explain usage of GraphQL, probably in the docs
        # Perhaps provide this API as public?
        data = {
            "method": "GET",
            "response_format": "json",
            "queries": _graphql.queries_to_json(*queries),
        }
        req_log.debug("Making GraphQL queries: %s", queries)
        return await self._post("/api/graphqlbatch/", data, as_graphql=True)

    async def _do_send_request(self, data):
        now = _util.now()
        offline_threading_id = _util.generate_offline_threading_id()
        data["client"] = "mercury"
        data["author"] = "fbid:{}".format(self._user_id)
        data["timestamp"] = _util.datetime_to_millis(now)
        data["source"] = "source:chat:web"
        data["offline_threading_id"] = offline_threading_id
        data["message_id"] = offline_threading_id
        data["threading_id"] = generate_message_id(now, self._client_id)
        data["ephemeral_ttl_mode:"] = "0"
        req_log.debug("POST /messaging/send/ <data redacted>")
        req_log.log(5, "Message data: %s", data)
        j = await self._post("/messaging/send/", data)

        _exception.handle_payload_error(j)

        try:
            message_ids = [
                (action["message_id"], action["thread_fbid"])
                for action in j["payload"]["actions"]
                if "message_id" in action
            ]
            if len(message_ids) != 1:
                log.warning("Got multiple message ids' back: {}".format(message_ids))
            return message_ids[0]
        except (KeyError, IndexError, TypeError) as e:
            raise _exception.ParseError("No message IDs could be found", data=j) from e
