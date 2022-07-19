from os import getenv
from aiohttp.web import Application, run_app
app = Application()
app.router.add_static('/files/', './static')
async def root_handler(request):
    return aiohttp.web.HTTPFound('https://google.com')
app.router.add_route('*', '/', root_handler)

run_app(app, port=int(getenv("PORT")))

