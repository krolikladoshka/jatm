import asyncio
from typing import Type, List

from aiohttp import web
from pydantic import BaseModel, ValidationError

from queue import schema
from queue.compute import compute, Task
from queue.router import router
from queue.schema import TaskStatus


class TaskManager:
    def __init__(self):
        self.task_queue = asyncio.Queue()
        self.shutdown_event = asyncio.Event()

    async def submit(self, task: schema):
        await self.task_queue.put(task)

        task.status = TaskStatus.enqueued

    async def list_tasks(self) -> List[Task]:
        return list(self.task_queue._queue)

    async def start(self, workers_count):
        workers = [asyncio.create_task(self.worker()) for i in range(workers_count)]

        await asyncio.gather(workers)

    async def worker(self):
        while not self.shutdown_event.is_set():
            task = await self.task_queue.get()

            await compute(task)

    async def stop(self):
        self.shutdown_event.set()


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
                print(e)

                raise web.HTTPBadRequest(body=e.json())

            return await func(request, validated_body, *args, **kwargs)
        return decorate
    return decorator


@router.post('/enqueue')
async def enqueue_task(request: web.Request, task_data: schema.SubmitTask):
    task_manager: TaskManager = request.app['task_manager']

    task = Task(**task_data.dict())
    await task_manager.submit(task)

    return web.Response(status=201)


@router.get('/')
async def list_tasks(request):
    task_manager: TaskManager = request.app['task_manager']

    return web.json_response(data=[task.dict() for task in await task_manager.list_tasks()])
