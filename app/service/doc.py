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


doc = Doc(
    state=state
)
