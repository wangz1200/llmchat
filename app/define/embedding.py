from .base import *


class EmbeddingEncodeReq(BaseModel):

    text: str | List[str]
    normalized: bool = True

