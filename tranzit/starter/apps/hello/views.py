import urllib
import asyncio
from tranzit import web


class IndexHandle(web.TZView):

    async def get(self, request):
        return web.Response(text='GET!')


class WSPullHandle(object):

    @staticmethod
    async def get_page(addr, *args, **kwargs):
        send_func = kwargs['send_func']
        writer = kwargs['writer']

        res = urllib.request.urlopen(addr).read(3000).decode('utf-8')

        await send_func(writer, res)


class WSPushHandle(object):

    @staticmethod
    async def get_hello(*args, **kwargs):
        send_func = kwargs['send_func']
        writer = kwargs['writer']

        while True:
            await asyncio.sleep(1)
            await send_func(writer, 'HELLO!')
