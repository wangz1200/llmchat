from .base import *


class UserItem(BaseModel):

    id: str | int | None = None
    user: str | int | None = None
    name: str | None = None
    password: str | None = None
    dept: str | int | None = None
    order: str | int | None = None
    create_by: str | int | None = None
    create_at: int | None = None


class UserReq(BaseModel):

    data: UserItem | List[UserItem]
    update: bool | None = None


class AddUserReq(BaseModel):

    data: UserItem | List[UserItem]
    update: bool | None = None

    def user_data(self):
        ret = []
        data = self.data
        if not isinstance(data, list):
            data = [data, ]
        ret.append(
            {
                "id": d["id"],
                "user": d["user"],
                "name": d["name"],
                "order": d["order"],
                "create_by": d["create_by"] or 0,
                "create_at": d["create_at"] or 0,
            }
            for d in data if d["id"] and d["user"] and d["name"]
        )
        return ret

    def password_data(self):
        ret = []
        data = self.data
        if not isinstance(data, list):
            data = [data, ]
        ret.append(
            {
                "id": d["id"],
                "password": d["password"],
            }
            for d in data if d["id"] and d["password"]
        )
        return ret

    def dept_data(self):
        ret = []
        data = self.data
        if not isinstance(data, list):
            data = [data, ]
        ret.append(
            {
                "id": d["id"],
                "dept": d["dept"],
            }
            for d in data if d["id"] and d["dept"]
        )
        return ret


class SetUserReq(BaseModel):

    data: UserItem | List[UserItem]
