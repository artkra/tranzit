import urllib
from tranzit import web


class IndexHandle(web.TZView):

    async def get(self, request):
        return web.Response(text='GET!')


class WSPullHandle(object):

    @staticmethod
    async def get_page(addr, *args, **kwargs):
        res = urllib.request.urlopen(addr).read(3000).decode('utf-8')

        return res

    @staticmethod
    async def get_hello(*args, **kwargs):

        return 'HELLO!'
