import os

from aiohttp import web

from task_queue import app as queue_app, TaskManager

PARALLEL_TASKS_COUNT = int(os.environ.get('PARALLEL_TASKS', 1))


app = web.Application()
app.add_subapp('/task_queue', queue_app)
app[queue_app['name']] = queue_app


async def start_task_manager(app: web.Application):
    app['task_queue']['task_manager'] = await TaskManager.create(PARALLEL_TASKS_COUNT)


async def shutdown_task_manager(app: web.Application):
    task_manager: TaskManager = app['task_manager']

    await task_manager.stop()


app.on_startup.append(start_task_manager)
app.on_shutdown.append(shutdown_task_manager)

web.run_app(app)
