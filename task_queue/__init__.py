from .router import router
from .views import *

app = web.Application()
app['name'] = 'task_queue'
app.add_routes(router)
