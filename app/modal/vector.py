from typing import Tuple, List, Dict, Any
from app import shared
from pymilvus import DataType


__all__ = (
    "Vector"
)


class Vector(object):

    def __init__(
            self,
            dim: int,
    ):
        self.mc = shared.vector.MilvusClient
        self.dim = dim

    def schema(self):

        schema_ = self.mc.create_schema(
            auto_id=False,
            enable_dynamic_field=False,
        )
        schema_.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_increment=False)
        schema_.add_field(field_name="pid", datatype=DataType.INT64)
        schema_.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=self.dim)
        schema_.add_field(field_name="text", datatype=DataType.VARCHAR)
        return schema_

    def index(self):
        index_params = self.mc.prepare_index_params()
        index_params.add_index(
            field_name="id",
            index_type="STL_SORT"
        )
        index_params.add_index(
            field_name="embedding",
            index_type="AUTOINDEX",
            metric_type="L2",
            params={
                "nlist": 1024,
            }
        )
        return index_params