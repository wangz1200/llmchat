from .base import *


class ChatReq(BaseModel):

    session_id: str | int | None = None
    system: str | None = None
    messages: list[Dict[str, str]] | None = None
    stream: bool = True
    knowledge: str | None = None


class ChatKnowledgeReq(ChatReq):

    knowledge: str
