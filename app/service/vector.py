from .base import *


__all__ = (
    "vector",
)


class Vector(object):

    def __init__(
            self,
            state: State | None = None,
    ):
        super().__init__()
        self.state = state

    def add(
            self,
            req: define.vector.AddVectorReq
    ):
        m = modal.vector.Milvus()
        data = req.data()
        for d in data:
            self.state.vector.create(
                name=d["name"],
                schema=m.schema(dim=d["dim"] or self.state.embedding.hidden_size),
                index=m.index(),
            )


vector = Vector(
    state=state
)

