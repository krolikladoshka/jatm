from pydantic import BaseModel, StrictInt, StrictFloat


class SubmitTask(BaseModel):
    n: StrictInt
    d: StrictFloat
    n1: StrictFloat
    interval: StrictFloat

    class Config:
        strict = True
