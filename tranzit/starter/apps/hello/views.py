from aiohttp import web

class IndexHandle(web.View):
    async def get(self):
        return 'HELLO'

    async def post(self):
        pass

    async def put(self):
        pass

    async def delete(self):
        pass