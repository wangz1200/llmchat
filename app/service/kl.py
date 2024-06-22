from .base import *
from app.service.doc import doc as svc_doc


__all__ = (
    "kl",
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
                collection = d["collection"]
                self.state.vector.create(
                    name=collection,
                    schema=modal.vector.Milvus.schema(dim=self.state.embedding.hidden_size),
                    index=modal.vector.Milvus.index(),
                )
            t_type = self.state.dao.table["kl_type"]
            stmt = self.state.dao.insert(t_type).values(data_)
            tx.execute(stmt)

    def delete(
            self,
            id_: str | int | List[str] | List[int] | None = None,
    ):
        if isinstance(id_, str):
            id_ = id_.split(",")
        if not isinstance(id_, list):
            id_ = [id_, ]
        if not id_:
            raise ValueError("文档类型ID号不能为空。")
        t_kl_type = self.state.dao.table["kl_type"]
        with self.state.dao.trans() as tx:
            stmt = self.state.dao.delete(t_kl_type)
            stmt = stmt.where(
                t_kl_type.c.id.in_(id_)
            )
            tx.execute(stmt)

    def list_(
            self,
            page_no: int | None = 0,
            page_size: int | None = 30,
    ):
        page_no = page_no or 0
        page_size = page_size or 30
        t_kl_doc = self.state.dao.table["kl_type"]
        t_kl_type = self.state.dao.table["kl_type"]
        with self.state.dao.trans() as tx:
            stmt = self.state.dao.select(
                t_kl_doc.c.id.label("doc_id"),
                t_kl_doc.c.pid.label("doc_pid"),
                t_kl_doc.c.name.label("doc_name"),
                t_kl_doc.c.type.label("doc_type"),
                t_kl_doc.c.create_by.label("user_id"),
                t_kl_doc.c.create_at.label("doc_create_at"),
                t_kl_type.c.collection.label("collection"),
                t_kl_type.c.name.label("doc_type_name"),
            ).select_from(
                t_kl_doc.join(t_kl_type, t_kl_type.c.id == t_kl_doc.c.pid)
            ).limit(
                page_size
            ).offset(
                page_size * (page_no - 1)
            )
            rows = self.state.dao.list_(
                tx.execute(stmt)
            )
        return rows


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
        doc_ = shared.doc.load_from_file(file_path)
        chunks = doc_.split(
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
            ret = self.state.vector.insert(
                name=collection,
                data=vector_data,
            )
        return ret

    def reset(
            self,
            id_: str | int | List[str] | List[int],
            chunk_size: int = 1000,
            override_size: int = 300,
    ):
        if isinstance(id_, str):
            id_ = id_.split(",")
        if not isinstance(id_, list):
            id_ = [id_, ]
        emb_ = svc_doc.embedding(
            kl_doc_id=id_,
            chunk_size=chunk_size,
            override_size=override_size,
        )
        if not emb_:
            raise Exception("向量化知识错误")
        for c, v in emb_.items():
            self.state.vector.insert(
                name=c,
                data=v,
            )

    def list_(
            self,
            page_no: int | None = 0,
            page_size: int | None = 30,
    ):
        page_no = page_no or 0
        page_size = page_size or 30
        t_kl_doc = self.state.dao.table["kl_type"]
        t_kl_type = self.state.dao.table["kl_type"]
        with self.state.dao.trans() as tx:
            stmt = self.state.dao.select(
                t_kl_doc.c.id.label("doc_id"),
                t_kl_doc.c.pid.label("doc_pid"),
                t_kl_doc.c.name.label("doc_name"),
                t_kl_doc.c.type.label("doc_type"),
                t_kl_doc.c.create_by.label("user_id"),
                t_kl_doc.c.create_at.label("doc_create_at"),
                t_kl_type.c.collection.label("collection"),
                t_kl_type.c.name.label("doc_type_name"),
            ).select_from(
                t_kl_doc.join(t_kl_type, t_kl_type.c.id == t_kl_doc.c.pid)
            ).limit(
                page_size
            ).offset(
                page_size * (page_no - 1)
            )
            rows = self.state.dao.list_(
                tx.execute(stmt)
            )
        return rows


kl = Knowledge(
    state=state
)

