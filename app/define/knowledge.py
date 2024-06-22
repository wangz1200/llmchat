from .base import *


class KlType(BaseModel):

    id: str | int | None = None
    pid: str | int | None = None
    collection: str | None = None
    name: str | None = None
    create_by: int | None = None
    create_at: int | None = None


class ResetKlReq(BaseModel):

    id: str | int | List[str] | List[int]


class AddKlTypeReq(BaseModel):

    data: KlType | List[KlType]


class GetKlTypeListReq(BaseModel):

    page_no: int | None = None
    page_size: int | None = None

