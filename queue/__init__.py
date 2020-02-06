from aiohttp import web
from .router import router
from .views import *

app = web.Application()

app.add_routes(router)