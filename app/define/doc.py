from .base import *


class DocFile(BaseModel):

    id: str | int | None = None
    pid: str | int | None = None
    name: str | None = None
    ext: str | None = None
    create_by: str | None = None
    create_at: str | None = None


class DocFolder(BaseModel):

    id: str | int | None = None
    pid: str | int | None = None
    name: str | None = None
    create_by: str | None = None
    create_at: str | None = None


class AddDocFileReq(BaseModel):

    data: DocFile | List[DocFile]
    update: bool | None = None

    def data_(self):
        data = self.data
        ret = []
        if not isinstance(data, list):
            data = [data, ]
        for d in data:
            d.id = d.id or shared.snow.sid()
            d.pid = d.pid or 0
            ret.append(d.model_dump())
        return ret


class UpdateDocFileReq(BaseModel):

    data: DocFile | List[DocFile]

    def data_(self):
        data = self.data
        if not isinstance(data, list):
            data = [data, ]
        ret = []
        for d in data:
            if not d.id:
                raise ValueError("ID不能为空。")
            ret.append(d.model_dump())
        return ret


class EmbDocFileReq(BaseModel):

    id: str | int
    chunk_size: int | None = 1000
    override_size: int | None = 300
    collection: str | None = None


class AddDocFolderReq(BaseModel):

    data: DocFolder | List[DocFolder]
    update: bool | None = None

    def data_(self):
        data = self.data
        ret = []
        if not isinstance(data, list):
            data = [data, ]
        for d in data:
            d.id = d.id or shared.snow.sid()
            d.pid = d.pid or 0
            ret.append(d.model_dump())
        return ret


class UpdateDocFolderReq(BaseModel):

    data: DocFolder | List[DocFolder]

    def data_(self):
        data = self.data
        if not isinstance(data, list):
            data = [data, ]
        ret = []
        for d in data:
            if not d.id:
                raise ValueError("ID不能为空。")
            ret.append(d.model_dump())
        return ret

    