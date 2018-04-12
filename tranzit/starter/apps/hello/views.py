import urllib
import time
import datetime
import asyncio
from tranzit import web


class IndexHandle(web.TZView):

    async def get(self, request):

        last_visit = request.session['last_visit'] if 'last_visit' in request.session else None
        ts = time.time()
        dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_visit'] = dt

        return web.Response(text='Last visit: {}'.format(last_visit))


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
