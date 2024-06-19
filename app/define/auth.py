from .base import *


class AuthReq(BaseModel):

    user: str
    password: str
    ad: bool | None = None
