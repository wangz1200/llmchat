from .base import *


__all__ = (
    "util",
)


class Util(object):

    def __init__(self):
        super().__init__()

    def list_(
            self,
            data: Any,
            separator: str = ","
    ):
        if data is None:
            return []
        if isinstance(data, str):
            data = data.split(separator)
        if not isinstance(data, list):
            data = [data, ]
        return data


util = Util()

