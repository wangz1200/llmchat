from .base import *
from .vector import vector as V


__all__ = (
    "knowledge",
)


class _Type(object):

    def __init__(
            self,
            state: State = state
    ):
        super().__init__()
        self.state = state

    def add(
            self,
            data: define.knowledge.KlType | List[define.knowledge.KlType],
    ):
        if not isinstance(data, list):
            data = [data, ]
        data_ = []
        for d in data:
            data_.append({
                "id": d.id or shared.snow.sid(),
                "pid": d.pid or 0,
                "name": d.name or "",
                "collection": d.collection or "",
                "create_by": d.create_by or 0,
                "create_at": d.create_at or 0,
            })
        with self.state.dao.trans() as tx:
            for d in data_:
                c_name = d["collection"]
                if c_name and self.state.vector.has_collection(c_name):
                    continue
                vm = modal.vector.Vector(
                    dim=self.state.embedding.hidden_size
                )
                self.state.vector.create_collection(
                    collection_name=c_name,
                    schema=vm.schema(),
                    index_params=vm.index(),
                )
            t_type = self.state.dao.table["kl_type"]
            stmt = self.state.dao.insert(t_type).values(data_)
            tx.execute(stmt)

    def delete(
            self,
            id_: str | int | List[str] | List[int] | None = None,
    ):
        pass

    def list_(
            self,
            page_no: int = 0,
            page_size: int = 30,
    ):
        pass


class Knowledge(object):

    def __init__(
            self,
            state: State = state
    ):
        super().__init__()
        self.state = state
        self.type_ = _Type(state=self.state)

    def get_info(
            self,
            id_: str | int | List[str] | List[int],
    ):
        t_type = self.state.dao.table["type"]
        t_doc = self.state.dao.table["doc"]
        stmt = self.state.dao.select(
            t_doc.c.id.label("id"),
            t_doc.c.title.label("title"),
            t_doc.c.ext.label("ext"),
            t_doc.c.create_at.label("create_at"),
            t_type.c.id.label("type_id"),
            t_type.c.name.label("type_name"),
        ).select_from(
            t_doc.outerjoin(t_type, t_type.c.id == t_doc.c.pid)
        )
        if not isinstance(id_, int):
            id_ = str(int)
        if not isinstance(id_, list):
            id_ = [id_]
        if id_:
            stmt = stmt.where(
                t_doc.c.id.in_(id_)
            )
        ret = self.state.dao.select(stmt)
        return ret

    def create(
            self,
            id_: str | int,
            ext: str,
            collection: str,
    ):
        doc_dir = Path(shared.config.args["root"]["path"], "public", "doc")
        file_name = f"{id_}.{ext}"
        file_path = doc_dir / file_name
        if not file_path.exists():
            raise FileNotFoundError(file_name)
        match ext.lower():
            case "txt":
                loader = FILE_MAP["txt"]
            case _:
                raise Exception("不支持的文件类型")
        file_loader = loader(file_path)
        chunks = file_loader.split(
            chunk_size=1000, overlap_size=300,
        )
        vector_data = []
        for chunk in chunks:
            emb = self.state.embedding.encode(text=chunk)
            emb = emb[0]["embedding"]
            vector_data.append({
                "id": shared.snow.sid(),
                "pid": id_,
                "embedding": emb,
                "text": chunk,
            })
        ret = None
        if vector_data:
            ret = V.insert(
                name=collection,
                data=vector_data,
            )
        return ret

    def reset(
            self,
            # data: define.knowledge.ResetKlReq,
            id_: str | int | List[str] | List[int],
    ):
        if isinstance(id_, str):
            id_ = id_.split(",")
        if not isinstance(id_, list):
            id_ = [id_, ]
        with self.state.dao.trans() as tx:
            t_kl_type = self.state.dao.table["kl_type"]
            t_kl_doc = self.state.dao.table["kl_doc"]
            stmt = self.state.dao.select(
                t_kl_doc.c.id.label("id"),
                t_kl_doc.c.pid.label("pid"),
                t_kl_doc.c.name.label("name"),
                t_kl_doc.c.ext.label("ext"),
                t_kl_type.c.collection.label("collection"),
            ).select_from(
                t_kl_doc.join(t_kl_type, t_kl_type.c.id == t_kl_doc.c.pid)
            ).where(
                t_kl_doc.c.id.in_(id_)
            )
            res = tx.execute(stmt)
            rows = self.state.dao.list_(res)
        for row in rows:
            self.create(
                id_=row["id"],
                ext=row["ext"],
                collection=row["collection"],
            )


knowledge = Knowledge(
    state=state
)

