from datetime import datetime
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
