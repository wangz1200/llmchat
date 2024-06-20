from .base import *


class LoginReq(BaseModel):

    user: str
    password: str
    ad: bool | None = None
