from tranzit import web


class IndexHandle(web.TZView):

    async def get(self, request):
        return web.Response(text='GET!')
