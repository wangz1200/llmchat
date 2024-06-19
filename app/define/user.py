from .base import *


class AddUserReq(BaseModel):

    user: str
    password: str
    dept: str | int | None = None