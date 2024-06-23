from .base import *


__all__ = (
    "embedding",
)


class Embedding(object):

    def __init__(
            self,
            state: State | None = None,
    ):
        super().__init__()
        self.state = state

    def encode(
            self,
            text: str | List[str],
            normalized: bool = True,
    ):
        return self.state.embedding.encode(
            text=text,
            normalized=normalized
        )


embedding = Embedding(
    state=state
)

