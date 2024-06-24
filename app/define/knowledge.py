from .base import *


class KlDoc(BaseModel):

    id: str | int | None = None
    pid: str | int | None = None
    name: str | None = None
    ext: str | None = None
    create_by: int | str | None = None
    create_at: int | str | None = None


class KlType(BaseModel):

    id: str | int | None = None
    pid: str | int | None = None
    name: str | None = None
    collection: str | None = None
    create_by: int | str | None = None
    create_at: int | str | None = None


class AddKlDocReq(BaseModel):

    data: KlDoc | List[KlDoc]
    update: bool | None = None

    def data_(self):
        data = self.data
        if not isinstance(data, list):
            data = [data, ]
        ret = []
        for d in data:
            d.id = d.id or shared.snow.sid()
            ret.append(d.model_dump())
        return ret


class AddKlTypeReq(BaseModel):

    data: KlType | List[KlType]
    update: bool | None = None

    def data_(self):
        data = self.data
        if not isinstance(data, list):
            data = [data, ]
        ret = []
        for d in data:
            d.id = d.id or shared.snow.sid()
            ret.append(d.model_dump())
        return ret

