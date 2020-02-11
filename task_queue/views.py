from typing import Type

from aiohttp import web
from pydantic import BaseModel, ValidationError

from task_queue import schema, util
from task_queue.router import router
from task_queue.tasks import TaskManager, Task


def validate_schema(schema: Type[BaseModel]):
    def decorator(func):
        async def decorate(request: web.Request, *args, **kwargs):
            try:
                body = await request.json()
            except:  # for simplicity
                raise web.HTTPBadRequest()

            try:
                validated_body = schema(**body)
            except ValidationError as e:
                raise web.HTTPBadRequest(body=e.json())

            return await func(request, validated_body, *args, **kwargs)

        return decorate

    return decorator


@router.post('/enqueue')
@validate_schema(schema.SubmitTask)
async def enqueue_task(request: web.Request, task_data: schema.SubmitTask):
    task_manager: TaskManager = request.app['task_manager']

    task = Task(**task_data.dict())
    await task_manager.submit(task)

    return web.Response(status=201)


@router.get('/')
async def list_tasks(request):
    task_manager: TaskManager = request.app['task_manager']

    return util.json_response(data=[task.dict() for task in await task_manager.list_tasks()])
