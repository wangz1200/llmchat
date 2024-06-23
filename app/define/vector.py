from .base import *


class AddVectorReq(BaseModel):

    name: str
    dim: int


class DeleteVectorReq(BaseModel):

    name: str

