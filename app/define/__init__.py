from typing import Any
from pydantic import BaseModel
from . import chat


class Result(BaseModel):

    code: int = 0
    msg: str = ""
    data: Any = None
