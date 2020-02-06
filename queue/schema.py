from datetime import datetime
from enum import Enum
from typing import Any, Dict

from pydantic import BaseModel


class SubmitTask(BaseModel):
    n: int
    d: float
    n1: float
    interval: float

    def materialize(self) -> Dict[str, Any]:
        result = self.dict()
        result['started'] = str(datetime.utcnow())

        return result


class TaskStatus(Enum):
    enqueued = 'enqueued'
    processed = 'processed'


class Task(BaseModel):
    status: TaskStatus
    n: int
    d: float
    n1: float
    current_value: float
    started_date: datetime
