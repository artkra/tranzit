# What's that?

<i><b>TRANZIT</b></i> is an asynchronous micro web framework supporting websockets
(full duplex socket communication). With <b>tranzit</b> you can easily maintain
both push & pull websocket messaging.

In fact, <b>tranzit</b> is a just a tony wrapper for wonderful
<b>aiohttp</b> lib providing async websocket server (which can be run
separately) and a little <i>CLI</i> tool.
 <!-- TODO: all the rest of README-->
## Installation
    $ pip install tranzit
## Quickstart
    $ tranzit project <PROJECT_NAME>
    $ cd <PROJECT_NAME>
    $ tranzit run

## Routing

## Config files

## Middlewares

## Using aiohttp module

## Few words about websockets

> <b>Warning:</b> <s>beware of yellow snow!</s> all websocket routes are
in the same namespace! Avoid collisions.

> <b>Another warning:</b> No security provided! Be sure to verify
websocket request (e.g. pass user session key in WS view parameters)


## Starting websocket server separately

