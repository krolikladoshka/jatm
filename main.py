from aiohttp import web
from queue import app as queue_app

app = web.Application()

app.add_subapp('queues', queue_app)

web.run_app(app)