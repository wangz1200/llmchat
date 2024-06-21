from .base import *


class Vector(object):

    def __init__(
            self,
            state: State = state
    ):
        super(Vector, self).__init__()
        self.state = state

    def add(
            self,
            name: str,
    ):
        if not self.state.vector.has_collection(
                collection_name=name,
        ):
            vector_modal = modal.vector.Vector(
                dim=self.state.embedding.hidden_size
            )
            schema = vector_modal.schema()
            index = vector_modal.index()
            self.state.vector.create_collection(
                collection_name=name,
                schema=schema,
                index_params=index,
            )

    def insert(
            self,
            name: str,
            data: Dict | List[Dict],
    ):
        ret = self.state.vector.insert(
            collection_name=name,
            data=data,
        )
        return ret


vector = Vector(
    state=state
)

