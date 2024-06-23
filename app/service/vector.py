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
            name: str,
            dim: int,
    ):
        m = modal.vector.Milvus()
        self.state.vector.create(
            name,
            schema=m.schema(dim=dim),
            index=m.index()
        )


vector = Vector(
    state=state
)

