from typing import Tuple, List, Dict, Any
from app import shared
from pymilvus import MilvusClient, DataType


__all__ = (
    "Vector"
)


class Milvus(object):

    @classmethod
    def schema(
            cls,
            dim: int
    ):
        schema_ = MilvusClient.create_schema(
            auto_id=False,
            enable_dynamic_field=False,
        )
        schema_.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_increment=False)
        schema_.add_field(field_name="pid", datatype=DataType.INT64)
        schema_.add_field(field_name="ext", datatype=DataType.VARCHAR, max_length=32)
        schema_.add_field(field_name="name", datatype=DataType.VARCHAR, max_length=512)
        schema_.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=dim)
        schema_.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=65535)
        return schema_

    @classmethod
    def index(cls):
        index_params = MilvusClient.prepare_index_params()
        index_params.add_index(
            field_name="embedding",
            index_type="IVF_FLAT",
            metric_type="L2",
            params={
                "nlist": 1024,
            }
        )
        return index_params
