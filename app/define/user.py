import requests

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


class AddUserReq(UserReq):

    update: bool | None = None

    def user(self):
        ret = []
        data = self.data
        if not isinstance(data, list):
            data = [data, ]
        for d in data:
            if not d.user or not d.name:
                raise ValueError("用户名及姓名未定义。")
            d.id = d.id or shared.snow.sid()
            d.order = d.order or 1
            d.create_by = d.create_by or 0
            d.create_at = d.create_at or 0
            ret.append({
                "id": d.id,
                "user": d.user,
                "name": d.name,
                "order": d.order,
                "create_by": d.create_by,
                "create_at": d.create_at,
            })
        return ret

    def password(self):
        ret = []
        data = self.data
        if not isinstance(data, list):
            data = [data, ]
        for d in data:
            if not d.id:
                raise ValueError("用户ID不能为空")
            d.password = d.password or "password"
            ret.append({
                "id": d.id,
                "password": d.password,
            })
        return ret

    def dept(self):
        ret = []
        data = self.data
        if not isinstance(data, list):
            data = [data, ]
        for d in data:
            if not d.id:
                raise ValueError("用户ID不能为空")
            d.dept = d.dept or 0
            ret.append({
                "user": d.id,
                "dept": d.dept,
            })
        return ret


class SetUserReq(UserReq):

    def user(self):
        ret = []
        data = self.data
        if not isinstance(data, list):
            data = [data, ]
        for d in data:
            if not d.id:
                raise ValueError("用户ID不能为空")
            row = {
                "id": d.id,
            }
            if d.user:
                row["user"] = d.user
            if d.name:
                row["name"] = d.name
            if d.order:
                row["order"] = d.order
            if d.create_by:
                row["create_by"] = d.create_by
            if d.create_at:
                row["create_at"] = d.create_at
            ret.append(row)
        return ret

    def password(self):
        ret = []
        data = self.data
        if not isinstance(data, list):
            data = [data, ]
        for d in data:
            if not d.id:
                raise ValueError("用户ID不能为空")
            row = {
                "id": d.id,
                "password": d.password or "password",
            }
            ret.append(row)
        return ret

    def dept(self):
        ret = []
        data = self.data
        if not isinstance(data, list):
            data = [data, ]
        for d in data:
            if not d.id:
                raise ValueError("用户ID不能为空")
            row = {
                "user": d.id,
                "dept": d.dept or 0,
            }
            ret.append(row)
        return ret

