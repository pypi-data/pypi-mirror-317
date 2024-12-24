``aiofbchat`` - Facebook Messenger for Python
=============================================

.. image:: https://badgen.net/badge/python/3.10,3.11,3.12?list=|
    :target: https://pypi.python.org/pypi/fbchat
    :alt: Supported python versions: 3.10, 3.11 and 3.12

.. image:: https://badgen.net/pypi/license/fbchat
    :target: https://github.com/togashigreat
    :alt: License: BSD 3-Clause

An Unofficial powerful and efficient library to interact with
`Facebook's Messenger <https://www.facebook.com/messages/>`__, using just your facebook account cookies
This is an asyncio fork of the `fbchat <https://github.com/carpedm20/fbchat>`__ library.

This is *not* an official API, Facebook has that `over here <https://developers.facebook.com/docs/messenger-platform>`__ for chat bots. This library differs by using a normal Facebook account instead.

``aiofbchat`` currently support:

- Fetching all messages, threads and images in threads.
- Searching for messages and threads.
- Creating groups, setting the group emoji, changing nicknames, creating polls, etc.
- Listening for, an reacting to messages and other events in real-time.
- Type hints, and it has a modern codebase (e.g. only Python 3.9 and upwards).
- ``async``/``await``

Essentially, everything you need to make an amazing Facebook bot!

.. note:: This verison is unstable some of the functionality may not work properly. I will fix them later when I have time.

Documentation
_____________

This is not Documented yet.



Usage
_______

A basic example of how you can use it.

.. code-block:: python 

  import asyncio
  import aiofbchat
  import json                                                                                         
  from aiofbchat._events import Connect, Disconnect
  from aiofbchat._events._delta_class import MessageEvent


  # use cookie exteniom in browser and get your facebook account cookies
  # and paste in a file and pass the coookie file path to this get_cookie fuction

  def get_cookie(path)-> dict:
      with open(path, "r") as f:
          data = json.load(f)
      cookies = {}
      for cookie in data:
        cookies[cookie["key"]] = cookie["value"]
      return cookies


  # Listen for new events and when that event is a new received message, reply to the author of the message
  async def listen(listener, session: aiofbchat.Session):
      async for event in listener.listen():
          if isinstance(event, Connect):
              print("AioFbchat is connected")

          if isinstance(event, MessageEvent):
              # If you're not the author, echo
              if event.author.id != session.user.id:
                  # reply_to_id replies to the given message id
                  await event.thread.send_message("Hello!", reply_to_id=event.message.id)

  async def main():
      # creating session from cookies
      session = await aiofbchat.Session.from_cookies(get_cookie("path to json"))
      # pass the cookies to client
      # you can use client to fetch other facebook users data
      client = aiofbchat.Client(session=session)

      # creatie a listener instance to listen to upcoming events (e.g. messages)
      # set chat_on to false if you dont want to show active status
      listener = aiofbchat.Listener(session=session, chat_on=True, foreground=True)

      # creating async tasm to run
      listen_task = asyncio.create_task(listen(listener, session))

      client.sequence_id_callback = listener.set_sequence_id

      # Call the fetch_threads API once to get the latest sequence ID
      await client.fetch_threads(limit=1).__anext__()

      # Let the listener run, otherwise the script will stop
      try:
          await listen_task
      except KeyboardInterrupt:
          await session._session.close()
      finally:
          await session._session.close()


  # run the main fuction and done
  asyncio.run(main())



