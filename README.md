# What's that?

_**TRANZIT**_ is an asynchronous micro web framework supporting websockets
(full duplex socket communication). With **tranzit** you can easily maintain
both push & pull websocket messaging.

In fact, **tranzit** is a just a tiny wrapper for wonderful
**aiohttp** lib providing async websocket server (which can be run
separately) and a little *CLI* tool.
 <!-- TODO: all the rest of README-->
## Installation

You can install **tranzit** via pip:

    $ pip install tranzit

## Quickstart

You can use *CLI* tool for that:

    $ tranzit project <PROJECT_NAME>
    $ cd <PROJECT_NAME>
    $ tranzit run

Now your project runs on http://0.0.0.0:3000/ .

The first command creates a skeleton project:

```
<PROJECT_NAME>/
    __init__.py
    apps/
        __init__.py
        hello/
            __init__.py
            static/
                camel.html
    common/
        static/
            tz.js
    main.py
    server.yml
```

The main.py file starts the whole thing. It gets configs from
*server.yml* such as:

* HTTP server host
* HTTP server port
* To start websocket server or not
* Websocket server host
* Websocket server port
* Which apps to run
* Is this a production start or not (not meaningful yet)

> **Info:** You should always pass PROJECT_DIR to *MainServer()*
constructor

## Routing and Views

All routing (for both http requests and websocket requests) is
handled by *apps/\<app_name>/routes.py* file.

`PATH_PREFIX` variable contains prefix for urls handled by this
application (like [http://0.0.0.0:3000/\<PATH_PREFIX>/some_url]).

`APP_STATIC_DIR` variable contains absolute path to the static
folder for this application.

All views for http requests are dispatched by *routes* dict.
Http views are ordinary **aiohttp** views.

All websocket views are dispatched by *ws_rules* dict.
See explanation below.

## Few words about websockets

To establish websocket messaging you must add websocket rule in
apps/\<app_name>/routes.py file just like that:

```python
ws_rules = {
    'get_hello': WSPushHandle.get_hello
}
```

Now this view is available via websockets.
To call this view function, do something like this on the
client side:

```javascript
var ws = new WebSocket('ws://0.0.0.0:19719');

ws.onmessage = function(response) {
    console.log(response.data);
};

ws.send('get_hello|');
```

We send message to call the view.
Here is an ugly syntax for that message:

`<function_name>|arg1, arg2, arg3, ... `

Now take a look at the websocket view:

```python
class WSPushHandle(object):

    @staticmethod
    async def get_hello(*args, **kwargs):
        send_func = kwargs['send_func']
        writer = kwargs['writer']

        while True:
            await asyncio.sleep(1)
            await send_func(writer, 'HELLO!')
```

Last line is a way to send message back to the client:

```python
            await send_func(writer, 'HELLO!')
```

As you can see, `send_func` and `writer` instances are accessible via `**kwargs`.


> **Warning:** ~~beware of yellow snow!~~ all websocket routes are
in the same namespace! Avoid collisions.

> **Another warning:** No security provided! Be sure to verify
websocket request (e.g. pass user session key in WS view parameters)


## Middlewares

> Will be implemented soon.

Then you will be able to pass list of your middlewares in *main.py*:
```python
MainServer(
    'server.yml', PROJECT_DIR, middlewares=[my_middleware]
)
```


## Using aiohttp module

All of `aiohttp.web` module is accessible via `tranzit.web`.

## Starting stand alone websocket server

You can use websocket server without http server.

All you need is an instance of:

*tranzit.web.WebSocketServer(host, port, api)*

*api* is a handler class instance which implements 3 functions
as shown below:

```python
class TranzitWSHandler(object):

    async def handle_text(self, loop, writer, msg):
        pass

    async def handle_binary(self, loop, writer, msg):
        pass

    async def handle_buffered(self, loop, reader, writer, first_msg):
        pass
```

Example starting stand alone websocket server:

```python
from tranzit.web import WebSocketServer


class MyHandler():
    def __init__(self, rules={}):
        self.rules = rules

    async def handle_text(self, loop, writer, msg):
        response = msg.upper()

        await WebSocketServer.send_text(writer, response)

    async def handle_binary(self, loop, writer, msg):
        pass

    async def handle_buffered(self, loop, reader, writer, first_msg):
        pass

ws_server = WebSocketServer(
    host='0.0.0.0', port=19719, api=MyHandler()
)

ws_server.run_forever()
```