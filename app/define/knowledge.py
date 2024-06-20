from .base import *


class ResetKnowledgeReq(BaseModel):

    doc_id: str | int | None = None
    knowledge: str | None = None

