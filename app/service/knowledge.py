from .base import *


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
            req: define.knowledge.AddKlTypeReq
    ):
        data = req.data_()
        if not data:
            raise ValueError("数据不能为空。")
        with self.state.dao.trans() as tx:
            t = self.state.dao.table["kl_type"]
            stmt = self.state.dao.insert(t).values(data)
            self.state.dao.execute(
                stmt=stmt, tx=tx,
            )

    def set_(
            self,
            data: Dict | List[Dict],
    ):
        if not isinstance(data, list):
            data = [data, ]
        t_kl_type = self.state.dao.table["kl_type"]
        stmt = self.state.dao.update(t_kl_type)
        with self.state.dao.trans() as tx:
            for d in data:
                id_ = d.pop("id", None)
                if not id_:
                    continue
                stmt_ = stmt.where(stmt.c.id == id_).values(**d)
                tx.execute(stmt_)

    def del_(
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
            stmt = self.state.dao.select(
                t_kl_type.c.collection
            ).where(
                t_kl_type.c.id.in_(id_)
            )
            rows = self.state.dao.list_(
                tx.execute(stmt)
            )
            names = [
                r["collection"] for r in rows
            ]
            self.state.vector.drop(
                name=names
            )
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
        t_kl_type = self.state.dao.table["kl_type"]
        source = self.state.dao.select(
            t_kl_type.c.id.label("id"),
            t_kl_type.c.pid.label("pid"),
            t_kl_type.c.name.label("name"),
            t_kl_type.c.collection.label("collection"),
            t_kl_type.c.create_by.label("create_by"),
            t_kl_type.c.create_at.label("create_at"),
        )
        with self.state.dao.trans() as tx:
            total = self.state.dao.execute(
                self.state.dao.select(sa.func.count(source.c.id))
            ).scalar()
            stmt = source.limit(
                page_size
            ).offset(
                page_size * (page_no - 1)
            )
            list_ = self.state.dao.list_(
                tx.execute(stmt)
            )
        return total, list_


class _Doc(object):

    def __init__(
            self,
            state: State | None = None,
    ):
        super().__init__()
        self.state = state

    def list_(
            self,
            id_: str | int | List[str] | List[int] | None = None,
            pid: str | int | List[str] | List[int] | None = None,
            page_no: int = 1,
            page_size: int = 30,
    ):
        t_kl_doc = self.state.dao.table["kl_doc"]
        t_kl_type = self.state.dao.table["kl_type"]
        source = self.state.dao.select(
            t_kl_doc.c.id.label("id"),
            t_kl_doc.c.pid.label("pid"),
            t_kl_doc.c.name.label("name"),
            t_kl_doc.c.ext.label("ext"),
            t_kl_doc.c.create_by.label("create_by"),
            t_kl_doc.c.create_at.label("create_at"),
            t_kl_type.c.name.label("type_name"),
            t_kl_type.c.collection.label("collection"),
        ).select_from(
            t_kl_doc.join(t_kl_type, t_kl_type.c.id == t_kl_doc.c.pid)
        )
        id_ = shared.util.list_(id_)
        if id_:
            source = source.where(
                t_kl_doc.c.id.in_(id_)
            )
        pid = shared.util.list_(pid)
        if pid:
            source = source.where(
                t_kl_type.c.id.in_(pid)
            )
        with self.state.dao.trans() as tx:
            total = self.state.dao.execute(
                stmt=self.state.dao.select(
                    sa.func.count(source.c.id)
                ),
                tx=tx,
            ).scalar()
            stmt = source.limit(page_size).offset(
                page_size * (page_no - 1)
            )
            list_ = self.state.dao.list_(
                self.state.dao.execute(
                    stmt=stmt, tx=tx
                )
            )
            return total, list_

    def add(
            self,
            req: define.knowledge.AddKlDocReq,
    ):
        data = req.data_()
        t_kl_doc = self.state.dao.table["kl_doc"]
        stmt = self.state.dao.insert(
            table=t_kl_doc,
            update=req.update
        ).values(data)
        self.state.dao.execute(
            stmt=stmt
        )

    def embedding(
            self,
            id_: str | int | List[str] | List[int],
            chunk_size: int = 1000,
            override_size: int = 300,
            insert: bool = False,
    ):
        id_ = shared.util.list_(id_)
        if not id_:
            raise ValueError("文档ID号错误")
        t_kl_doc = self.state.dao.table["kl_doc"]
        t_kl_type = self.state.dao.table["kl_type"]
        with self.state.dao.trans() as tx:
            stmt = self.state.dao.select(
                t_kl_doc.c.id.label("id"),
                t_kl_doc.c.name.label("name"),
                t_kl_doc.c.ext.label("ext"),
                t_kl_type.c.collection.label("collection"),
            ).select_from(
                t_kl_doc.join(t_kl_type, t_kl_type.c.id == t_kl_doc.c.pid)
            ).where(
                t_kl_doc.c.id.in_(id_)
            )
            res = tx.execute(stmt)
            rows = self.state.dao.list_(rows=res)
        file_dir = shared.config.args["root"]["path"]
        data = {}
        for row in rows:
            id_ = row["id"]
            ext = row["ext"]
            cn = row["collection"]
            file_name = f"{id_}.{ext}"
            doc_ = shared.doc.load_from_file(
                file_path=Path(file_dir, "public", "doc", file_name)
            )
            chunks = doc_.split(
                chunk_size=chunk_size,
                overlap_size=override_size,
            )
            embedding = self.state.embedding.encode(
                text=chunks
            )
            item = data.get(cn, [])
            for i, emb in enumerate(embedding):
                item.append({
                    "id": shared.snow.sid(),
                    "pid": id_,
                    "embedding": emb["embedding"],
                    "text": chunks[i],
                })
            if insert and item:
                m = modal.vector.Milvus()
                self.state.vector.create(
                    name=cn,
                    schema=m.schema(dim=self.state.embedding.hidden_size),
                    index=m.index(),
                )
                self.state.vector.insert(
                    name=cn,
                    data=item,
                )
            data[cn] = item
        return data

    def reset(
            self,
            req: define.knowledge.ResetDocReq
    ):
        id_ = shared.util.list_(
            data=req.id
        )
        if not id_:
            raise ValueError("文档ID号不能为空。")
        t = self.state.dao.table["kl_doc"]
        stmt = self.state.dao.select(t).where(
            t.c.id.in_(id_)
        )
        list_ = self.state.dao.list_(
            self.state.dao.execute(stmt)
        )
        if not list_:
            return
        data = self.embedding(
            id_=id_,
            chunk_size=req.chunk_size,
            override_size=req.override_size,
            insert=True,
        )
        return data


class Knowledge(object):

    def __init__(
            self,
            state: State = state
    ):
        super().__init__()
        self.state = state
        self.type_ = _Type(
            state=self.state,
        )
        self.doc = _Doc(
            state=self.state,
        )

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

    def get(
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

    def set_(
            self,
            data: Dict | List[Dict],
    ):
        if not isinstance(data, list):
            data = [data, ]
        t_kl_doc = self.state.dao.table["kl_doc"]
        stmt = self.state.dao.update(t_kl_doc)
        with self.state.dao.trans() as tx:
            for d in data:
                id_ = d.pop("id", None)
                if not id_:
                    continue
                stmt_ = stmt.where(stmt.c.id == id_).values(**d)
                tx.execute(stmt_)

    def del_(
            self,
            id_: str | int | List[str] | List[int] | None = None
    ):
        id_ = shared.util.list_(id_)
        if not id_:
            raise ValueError("ID号不能为空。")
        t_kl_doc = self.state.dao.table["kl_doc"]

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
        emb_ = self.doc.embedding(
            id_=id_,
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


knowledge = Knowledge(
    state=state
)

