from .base import *


__all__ = (
    "doc",
)


class Doc(object):

    def __init__(
            self,
            state: State | None = None,
    ):
        super().__init__()
        self.state = state

    def embedding(
            self,
            kl_doc_id: str | int | List[str] | List[int],
            chunk_size: int = 1000,
            override_size: int = 300,
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
        file_dir = shared.config.args["root"]["path"]
        data = {}
        for row in rows:
            id_ = row["id"]
            ext = row["ext"]
            cn = row["collection"]
            file_name = f"{id_}.{ext}"
            doc_ = shared.doc.load_from_file(
                file_path=Path(file_dir, file_name)
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
            data[cn] = item
        return data


doc = Doc(
    state=state,
)

