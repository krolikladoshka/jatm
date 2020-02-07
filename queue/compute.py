import asyncio
import dataclasses
from dataclasses import dataclass, field
from datetime import datetime

from queue.schema import TaskStatus


@dataclass
class Task:
    status: TaskStatus = field(init=False)

    n: int
    d: float
    n1: float
    interval: float

    v: float = field(init=False)

    started_datetime: datetime = field(init=False, default=datetime.utcnow())

    def __post_init__(self):
        self.v = self.n1

    def dict(self):
        return dataclasses.asdict(self)


async def compute(task: Task):
    for i in range(task.n):
        await asyncio.sleep(task.interval)

        task.v += task.d
