import sys
from typing import List, Dict
from pymilvus import MilvusClient, CollectionSchema
from pymilvus.milvus_client import IndexParams


__all__ = (
    "Milvus",
)


class Milvus(object):

    def __init__(
            self,
            host: str = "127.0.0.1",
            port: int = 19530,
            name: str = "default",
            **kwargs,
    ):
        super().__init__()
        uri = f"http://{host}:{port}"
        self.client = MilvusClient(
            uri=uri,
            db_name=name,
            **kwargs,
        )

    def create(
            self,
            name: str,
            schema: CollectionSchema,
            index: IndexParams,
    ):
        if not self.client.has_collection(
                collection_name=name,
        ):
            self.client.create_collection(
                collection_name=name,
                schema=schema,
                index_params=index,
            )

    def drop(
            self,
            name: str | List[str],
    ):
        if not isinstance(name, list):
            name = [name, ]
        for n in name:
            self.client.drop_collection(
                collection_name=n,
            )

    def search(
            self,
            name: str,
            embedding: List[float] | List[List[float]],
            output_fields: list[str] | None = None,
            score: float = 0.8,
            limit: int = 5,
    ):
        if not output_fields:
            output_fields = ["id", "pid", "text"]
        if not isinstance(embedding[0], list):
            embedding = [embedding, ]
        res = self.client.search(
            collection_name=name,
            data=embedding,
            limit=limit,
            output_fields=output_fields,
            search_params={
                "metric_type": "L2",
                "params": {
                    "range_filter": 0,
                    "radius": score,
                },
            }
        )
        ret = []
        for r in res:
            ret += r
        return ret

    def insert(
            self,
            name: str,
            data: Dict | List[Dict],
    ):
        ret = self.client.insert(
            collection_name=name,
            data=data,
        )
        return ret

    def delete(
            self,
            name: str,
            id_: str | int | List[str] | List[int] | None = None,
            pid: str | int | List[str] | List[int] | None = None,
    ):
        if id_:
            if isinstance(id_, str):
                id_ = id_.split(",")
            if not isinstance(id_, list):
                id_ = [id_, ]
        else:
            id_ = None
        if pid:
            if isinstance(pid, str):
                pid = pid.split(",")
            if not isinstance(pid, list):
                pid = [pid, ]
            filter_ = f"pid in [{','.join(pid)}]"
        else:
            filter_ = ""
        self.client.delete(
            collection_name=name,
            ids=id_,
            filter=filter_,
        )

