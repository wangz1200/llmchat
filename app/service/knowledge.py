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

    def create(
            self,
            name: str,
            collection: str,
            id_: str | int | None = None,
            user_id: str | int | None = None,
            pid: str | int = 0,
    ):
        with self.state.dao.trans() as tx:
            if not self.state.vector.has_collection(collection):
                vector_modal = modal.vector.Vector(
                    dim=self.state.embedding.hidden_size
                )
                schema = vector_modal.schema()
                index = vector_modal.index()
                self.state.vector.create_collection(
                    collection_name=collection,
                    schema=schema,
                    index_params=index,
                )
            t_type = self.state.dao.table["kl_type"]
            id_ = id_ or shared.snow.sid()
            create_by = user_id or 0
            create_at = 0
            stmt = self.state.dao.insert(t_type).values({
                "id": id_,
                "pid": pid or 0,
                "name": name,
                "create_by": create_by,
                "create_at": create_at,
            })
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

    def reset(
            self,
            id_: str | int,
            collection: str,
    ):
        info = self.get_info(
            id_=id_,
        )
        if not info:
            raise Exception("当前文档不存在")


knowledge = Knowledge(
    state=state
)

