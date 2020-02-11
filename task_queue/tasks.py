import asyncio
import dataclasses
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List

from task_queue.compute import compute


class TaskStatus(str, Enum):
    enqueued = 'enqueued'
    processing = 'processing'

    def __str__(self):
        return f'{self.name}'


@dataclass
class Task:
    status: TaskStatus = field(init=False)

    n: int
    d: float
    n1: float
    interval: float

    v: float = field(init=False)

    started_datetime: datetime = field(init=False)

    def __post_init__(self):
        self.v = self.n1
        self.started_datetime = datetime.utcnow()

    def dict(self):
        return dataclasses.asdict(self)


class TaskManager:
    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        self._loop = loop or asyncio.get_running_loop()
        self.task_queue = asyncio.Queue(loop=self._loop)
        self.shutdown_event = asyncio.Event(loop=self._loop)
        self.processing_tasks = deque()

    async def submit(self, task: Task):
        await self.task_queue.put(task)

        task.status = TaskStatus.enqueued

    async def list_tasks(self) -> List[Task]:
        return list(self.task_queue._queue) + list(self.processing_tasks)

    def start(self, workers_count: int) -> 'TaskManager':
        self._start_task = asyncio.create_task(self._start(workers_count))

        return self

    async def _start(self, workers_count):
        workers = [asyncio.create_task(self.worker()) for i in range(workers_count)]

        await asyncio.gather(workers)

    async def worker(self):
        while not self.shutdown_event.is_set():
            task = await self.task_queue.get()
            self.processing_tasks.append(task)
            await compute(task)
            self.processing_tasks.popleft()

    async def stop(self):
        self.shutdown_event.set()

        await self._start_task

    @classmethod
    async def create(cls, tasks_count):
        manager = cls()

        return manager.start(tasks_count)
