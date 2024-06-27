from .base import *


class ChatReq(BaseModel):

    id: str | int | None = None
    sid: str | int | None = None
    pid: str | int = 0
    messages: Dict | List[Dict] | None = None
    model: str | None = None
    max_tokens: int | None = None
    stream: bool = True
    temperature: float = 0.0
    knowledge: str | None = None
    log: bool = False


class ChatToolReq(BaseModel):

    id: str | int | None = None
    sid: str | int | None = None
    pid: str | int = 0
    messages: Dict | List[Dict] | None = None
    model: str | None = None
    max_tokens: int | None = None
    stream: bool = True
    temperature: float = 0.0
    knowledge: str | None = None
    log: bool = False
