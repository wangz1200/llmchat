import sys
import pymilvus as pm
from pymilvus import MilvusClient


__all__ = (
    "Milvus",
    "MilvusClient",
)


class Milvus(object):

    def __init__(
            self,
            host: str = "127.0.0.1",
            port: int | str = 19530,
            name: str = "default",
    ):
        super().__init__()
        self._name = name
        port = int(port)
        pm.connections.connect(
            host=host,
            port=port,
            db_name=name,
        )

    @property
    def name(self):
        return self._name

    def collection(
            self,
            name: str,
            *fields,
            **kwargs,
    ):
        schema = pm.CollectionSchema(
            fields=list(fields),
            description="collection description",
        ) if fields else None
        c = pm.Collection(
            name=name,
            schema=schema,
            **kwargs,
        )
        return c

    def has_schema(
            self,
            collection: str,
    ):
        return pm.utility.has_collection(
            collection_name=collection,
        )

    def load(
            self,
            collection: str,
    ):
        pm.Collection(
            name=collection
        ).load()

    def create_index(
            self,
            collection: str,
            field: str = "embedding",
            **kwargs,
    ):
        index = {
            "metric_type": kwargs.get("metric_type", "L2"),
            "index_type": kwargs.get("index_type", "IVF_FLAT"),
            "params": {
                "nlist": kwargs.get("nlist", 2048),
            },
        }
        status = pm.Collection(name=collection).create_index(
            field_name=field,
            index_params=index
        )
        return status

    def insert(
            self,
            name: str,
            vectors,
    ):
        data = [vectors]
        mr = pm.Collection(
            name=name
        ).insert(data)
        ids = mr.primary_keys
        return ids

    def search(
            self,
            name: str,
            vectors,
            anns_field: str = "embedding",
            top_k: int = 5,
            metric_type: str = "L2",
            nprobe: int = 16,
            **kwargs,
    ):
        params = {
            "metric_type": metric_type,
            "params": {
                "nprobe": nprobe,
            }
        }
        res = pm.Collection(name=name).search(
            data=vectors,
            anns_field=anns_field,
            param=params,
            limit=top_k,
        )
        return res

    def count(
            self,
            name: str,
    ):
        c = pm.Collection(name=name)
        c.flush()
        num = c.num_entities
        return num

    def drop(
            self,
            name: str,
    ):
        c = pm.Collection(name=name)
        if c:
            c.drop()


if __name__ == "__main__":
    milvus = Milvus(
        host="127.0.0.1",
        port=19530,
    )
    MilvusClient(

    )

    pass


