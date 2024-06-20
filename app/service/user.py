from .base import *


__all__ = (
    "user",
)


class _Password(object):

    def __init__(
            self,
            state: State = state,
    ):
        super().__init__()
        self.state = state
        self.dao = self.state.dao

    def set_(
            self,
            user_: str,
            password: str,
            tx=None,
    ):
        t_password = self.dao.table["password"]
        stmt = sa.insert(t_password).values()


class User(object):

    def __init__(
            self,
            state: State = state
    ):
        super().__init__()
        self.state = state
        self.dao = self.state.dao
        self.password = _Password(
            state=self.state
        )

    def login(
            self,
            user_: str,
            password: str,
    ):
        t_user = self.dao.table["user"]
        t_password = self.dao.table["password"]
        stmt = self.dao.select(
            t_user.c.id.label("id"),
            t_user.c.user.label("user"),
            t_user.c.name.label("name"),
            sa.or_(t_password.c.password, "abc123").label("password"),
        ).select_from(
            t_user.outjoin(t_password, t_user.c.id == t_password.c.user)
        ).where(
            t_user.c.user == user_
        )
        res = self.dao.list_(
            rows=self.dao.execute(stmt)
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
            "authority": token,
        }


user = User(
    state=state
)

