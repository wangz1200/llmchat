import sys
import pymilvus as pm


class MilvusConnection(object):

    def __init__(
            self,
            host: str = "127.0.0.1",
            port: int = 19530,
            name: str = "default",
    ):
        super().__init__()
        pm.connections.connect(
            host=host,
            port=port,
        )
        self._name = name
        self.collection = pm.Collection(
            name=self.name,
        )
        self.collection.load()

    @property
    def name(self) -> str:
        return self._name

    def create_schema(
            self,
            *fields: pm.FieldSchema,
            **kwargs,
    ):
        schema = pm.CollectionSchema(
            fields=list(fields),
            description="collection description",
        )
        self.collection = pm.Collection(
            name=self.name,
            schema=schema,
        )

    def has_schema(self):
        return pm.utility.has_collection(
            collection_name=self.name,
        )

    def create_index(
            self,
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
        status = self.collection.create_index(
            field_name=field,
            index_params=index
        )
        return status

    def insert(
            self,
            vectors,
    ):
        data = [vectors]
        mr = self.collection.insert(data)
        ids = mr.primary_keys
        return ids

    def search(
            self,
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
        res = self.collection.search(
            data=vectors,
            anns_field=anns_field,
            param=params,
            limit=top_k,
        )
        return res

    def count(self):
        self.collection.flush()
        num = self.collection.num_entities
        return num

    def delete(self):
        if self.collection:
            self.collection.drop()


if __name__ == "__main__":
    conn = MilvusConnection(
        host="127.0.0.1",
        port=19530,
    )

    pass


