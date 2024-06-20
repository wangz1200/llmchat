from typing import List, Dict, Any
from pydantic import BaseModel


class UploadDocReq(BaseModel):

    name: str | None = None
    