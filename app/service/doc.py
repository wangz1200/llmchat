from .base import *


__all__ = (
    "doc",
)


class Doc(object):

    def __init__(
            self,
            state: State = state,
    ):
        super().__init__()
        self.state = state
        self.dao = self.state.dao
        self.vector = self.state.vector

    def load(
            self,
            file_path: str | Path,
    ):
        pass

    def load_file(
            self,
            id_: int | str,
            ext: str,
    ):
        file_dir = shared.config.args["root"]["path"]
        file_name = f"{id_}.{ext}"
        file_path = Path(file_dir, file_name)
        match ext.lower():
            case "txt":
                loader = shared.doc.Text
            case _:
                raise Exception("不支持的文档类型")
        return loader(file_path)

    def embedding(
            self,
            kl_doc_id: str | int | List[str] | List[int],
    ):
        if isinstance(kl_doc_id, str):
            kl_doc_id = kl_doc_id.split(",")
        if not kl_doc_id:
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
                t_kl_doc.c.id.in_(kl_doc_id)
            )
            res = tx.execute(stmt)
            rows = self.state.dao.list_(rows=res)
        data = {}
        for row in rows:
            id_ = row["id"]
            ext = row["ext"]
            cn = row["collection"]
            doc_ = self.load_file(
                id_=id_, ext=ext,
            )
            item = data.get(cn, [])


doc = Doc(
    state=state
)
