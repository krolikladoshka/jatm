from .router import router
from .views import *

app = web.Application()
app['name'] = 'queue'
app.add_routes(router)
