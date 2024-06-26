from typing import Any
from pydantic import BaseModel
from . import auth
from . import user
from . import doc
from . import embedding
from . import knowledge
from . import vector
from . import chat


class Result(BaseModel):

    code: int = 0
    msg: str = ""
    data: Any = None
