from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, StrictInt, StrictFloat


class SubmitTask(BaseModel):
    n: StrictInt
    d: StrictFloat
    n1: StrictFloat
    interval: StrictFloat

    def materialize(self) -> Dict[str, Any]:
        result = self.dict()
        result['started'] = str(datetime.utcnow())

        return result

    class Config:
        strict = True
