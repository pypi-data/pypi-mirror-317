import sys
from attrs import define
import logging

log = logging.getLogger("fbchat")
req_log = logging.getLogger("fbchat.request")


kw_only = sys.version_info[:2] > (3, 5)


#: Default attrs settings for classes
attrs_default = define(frozen=True, slots=True, kw_only=True, auto_attribs=True)
