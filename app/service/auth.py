from .base import *
from .user import user as svc_user


__all__ = (
    "auth",
)


class _AD(object):

    def __init__(
            self,
            url: str,
    ):
        super().__init__()
        self.url = url

    def verify(
            self,
            user: str,
            password: str,
    ):
        pass


class Auth(object):

    def __init__(
            self,
            state: State = state,
    ):
        super().__init__()
        self.state = state

    def verify(
            self,
            user: str,
            password: str,
    ):
        t_user = self.state.dao.table["user"]
        t_password = self.state.dao.table["password"]
        stmt = self.state.dao.select(
            t_user.c.id.label("id"),
            t_user.c.user.label("user"),
            t_user.c.name.label("name"),
            sa.or_(t_password.c.password, "abc123").label("password"),
        ).select_from(
            t_user.outjoin(t_password, t_user.c.id == t_password.c.user)
        ).where(
            t_user.c.user == user
        )
        res = self.state.dao.list_(
            rows=self.state.dao.execute(stmt)
        )
        if len(res) == 0:
            raise Exception("用户不存在。")
        res = res[0]
        if password != res["password"]:
            raise Exception("密码错误。")
        token = shared.token.build(
            user=res["user"]
        )
        return {
            "token": token,
        }

    def login(
            self,
            user: str,
            password: str,
            method: str = "",
    ):
        return self.verify(
            user=user,
            password=password,
        )


auth = Auth(
    state=state,
)

