from .base import *


class ChatReq(BaseModel):

    id: str | int | None = None
    sid: str | int | None = None
    messages: Dict[str, str] | list[Dict[str, str]] | None = None
    stream: bool = True
    knowledge: str | None = None
