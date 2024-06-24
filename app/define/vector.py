from .base import *


class Vector(BaseModel):

    name: str
    dim: int | None = None


class AddVectorReq(BaseModel):

    data: Vector | List[Vector]

    def data(self):
        data = self.data
        if not isinstance(data, list):
            data = [data, ]
        ret = [
            d.model_dump()
            for d in data
        ]
        return ret


class DeleteVectorReq(BaseModel):

    name: str

