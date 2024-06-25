from .base import *


class _File(object):

    def __init__(
            self,
            state: State,
    ):
        super().__init__()
        self.state = state

    def query(
            self,
            id_: str | int | List[str] | List[int] | None = None,
    ):
        pass

    def add(
            self,
            req: define.doc.AddDocFileReq,
            tx: sa.Connection | None = None,
    ):
        data = req.data_()
        if not data:
            raise ValueError("数据不能为空。")
        t = self.state.dao.table["doc_file"]
        stmt = self.state.dao.insert(t).values(data)
        self.state.dao.execute(
            stmt=stmt, tx=tx,
        )

    def update(
            self,
            req: define.doc.UpdateDocFileReq,
            tx: sa.Connection | None = None,
    ):
        def _action(tx, stmt, data):
            for d in data:
                id_ = d.pop("id", None)
                if not id_ or not d:
                    continue
                tx.execute(
                    stmt.values(**d).where(t.c.id == id_)
                )
        data = req.data_()
        if not data:
            raise ValueError("数据不能为空。")
        t = self.state.dao.table["doc_file"]
        stmt = self.state.dao.update(t)
        if tx:
            _action(tx=tx, stmt=stmt, data=data)
        else:
            with self.state.dao.trans() as tx:
                _action(tx=tx, stmt=stmt, data=data)

    def remove(
            self,
            id_: str | int | List[int] | List[str],
            tx: sa.Connection | None = None,
    ):
        id_ = shared.util.list_(id_)
        if not id_:
            raise ValueError("ID号不能为空。")
        t = self.state.dao.table["doc_file"]
        stmt = self.state.dao.delete(t).where(
            t.c.id.in_(id_)
        )
        self.state.dao.execute(
            stmt=stmt, tx=tx,
        )

    def list_(
            self,
            id_: str | int | List[str] | List[int] | None = None,
            pid: str | int | List[str] | List[int] | None = None,
            page_no: int = 1,
            page_size: int = 30,
    ):
        t_doc_file = self.state.dao.table["doc_file"]
        t_doc_folder = self.state.dao.table["doc_folder"]
        source = self.state.dao.select(
            t_doc_file.c.id.label("id"),
            t_doc_file.c.pid.label("pid"),
            t_doc_file.c.name.label("name"),
            t_doc_file.c.ext.label("ext"),
            t_doc_file.c.create_by.label("create_by"),
            t_doc_file.c.create_at.label("create_at"),
            t_doc_folder.c.name.label("type_name"),
            t_doc_folder.c.collection.label("collection"),
        ).select_from(
            t_doc_file.join(t_doc_folder, t_doc_folder.c.id == t_doc_file.c.pid)
        )
        id_ = shared.util.list_(id_)
        if id_:
            source = source.where(
                t_doc_file.c.id.in_(id_)
            )
        pid = shared.util.list_(pid)
        if pid:
            source = source.where(
                t_doc_file.c.pid.in_(pid)
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

    def embedding(
            self,
            req: define.doc.EmbDocFileReq
    ):
        id_ = shared.util.list_(req.id)
        if not id_:
            raise ValueError("文档ID号错误")
        t_doc_file = self.state.dao.table["doc_file"]
        with self.state.dao.trans() as tx:
            stmt = self.state.dao.select(
                t_doc_file
            ).where(
                t_doc_file.c.id.in_(id_)
            )
            res = tx.execute(stmt)
            rows = self.state.dao.list_(rows=res)
        file_dir = shared.config.args["root"]["path"]
        data = []
        for row in rows:
            id_ = row["id"]
            pid = row["pid"]
            ext = row["ext"]
            name = row["name"]
            file_name = f"{id_}.{ext}"
            doc_ = shared.doc.load_from_file(
                file_path=Path(file_dir, "public", "doc", file_name)
            )
            chunks = doc_.split(
                chunk_size=req.chunk_size or 1000,
                overlap_size=req.override_size or 300,
            )
            embedding = self.state.embedding.encode(
                text=chunks
            )
            for i, emb in enumerate(embedding):
                data.append({
                    "id": shared.snow.sid(),
                    "pid": pid,
                    "ext": ext,
                    "name": name,
                    "embedding": emb["embedding"],
                    "text": chunks[i],
                })
        if req.collection and data:
            m = modal.vector.Milvus()
            self.state.vector.create(
                name=req.collection,
                schema=m.schema(dim=self.state.embedding.hidden_size),
                index=m.index(),
            )
            self.state.vector.insert(
                name=req.collection,
                data=data,
            )
        return data


class _Folder(object):

    def __init__(
            self,
            state: State,
    ):
        super().__init__()
        self.state = state

    def add(
            self,
            req: define.doc.AddDocFolderReq,
            tx: sa.Connection | None = None
    ):
        data = req.data_()
        if not data:
            raise ValueError("数据不能为空")
        t = self.state.dao.table["doc_folder"]
        stmt = self.state.dao.insert(t).values(data)
        if tx:
            tx.execute(stmt)
        else:
            with self.state.dao.trans() as tx:
                tx.execute(stmt)

    def update(
            self,
            req: define.doc.UpdateDocFolderReq,
            tx: sa.Connection | None = None,
    ):
        def _action(tx, stmt, data):
            for d in data:
                id_ = d.pop("id", None)
                if not id_ or not d:
                    continue
                tx.execute(
                    stmt.values(**d).where(t.c.id == id_)
                )
        data = req.data_()
        if not data:
            raise ValueError("数据不能为空。")
        t = self.state.dao.table["doc_folder"]
        stmt = self.state.dao.update(t)
        if tx:
            _action(tx=tx, stmt=stmt, data=data)
        else:
            with self.state.dao.trans() as tx:
                _action(tx=tx, stmt=stmt, data=data)

    def remove(
            self,
            id_: str | int | List[int] | List[str],
            tx: sa.Connection | None = None,
    ):
        id_ = shared.util.list_(id_)
        if not id_:
            raise ValueError("ID号不能为空。")
        t = self.state.dao.table["doc_folder"]
        stmt = self.state.dao.delete(t).where(
            t.c.id.in_(id_)
        )
        self.state.dao.execute(
            stmt=stmt, tx=tx,
        )

    def list_(
            self,
            id_: str | int | List[str] | None = None,
            page_no: int | None = 0,
            page_size: int | None = 30,
    ):
        page_no = page_no or 0
        page_size = page_size or 30
        t_doc_folder = self.state.dao.table["doc_folder"]
        source = self.state.dao.select(
            t_doc_folder.c.id.label("id"),
            t_doc_folder.c.pid.label("pid"),
            t_doc_folder.c.name.label("name"),
            t_doc_folder.c.create_by.label("create_by"),
            t_doc_folder.c.create_at.label("create_at"),
        )
        id_ = shared.util.list_(id_)
        if id_:
            source = source.where(
                t_doc_folder.c.id.in_(id_)
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


class Doc(object):

    def __init__(
            self,
            state: State | None = None,
    ):
        super().__init__()
        self.state = state
        self.folder = _Folder(
            state=self.state,
        )
        self.file = _File(
            state=self.state,
        )


doc = Doc(
    state=state
)
