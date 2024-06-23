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

    def _prepare(
            self,
            req: define.user.UserReq
    ):
        ret = []
        data = req.data
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

    def add(
            self,
            req: define.user.UserReq,
            tx: sa.Connection | None = None,
    ):
        data = self._prepare(req=req)
        if not data:
            return
        t = self.dao.table["password"]
        stmt = self.state.dao.insert(
            t, update=req.update
        ).values(data)
        self.state.dao.execute(
            stmt=stmt,
            tx=tx
        )

    def set_(
            self,
            req: define.user.UserReq,
            tx: sa.Connection | None = None,
    ):
        data = self._prepare(req=req)
        if not data:
            return
        t = self.dao.table["password"]
        for d in data:
            stmt = self.state.dao.update(t).values(d)
            self.state.dao.execute(stmt=stmt, tx=tx)


class _Dept(object):

    def __init__(
            self,
            state: State = state,
    ):
        super().__init__()
        self.state = state
        self.dao = self.state.dao

    def add(
            self,
            req: define.user.UserReq,
            tx: sa.Connection | None = None,
    ):
        ret = []
        data = req.data
        if not isinstance(data, list):
            data = [data, ]
        ret.append(
            {
                "id": d["id"],
                "dept": d["dept"],
            }
            for d in data if d["id"] and d["dept"]
        )
        if not ret:
            return
        t = self.dao.table["user_dept"]
        stmt = self.state.dao.insert(
            t, update=req.update
        ).values(data)
        self.state.dao.execute(
            stmt=stmt,
            tx=tx
        )

    def set_(
            self,
            req: define.user.UserReq,
    ):
        pass


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
        self.dept = _Dept(
            state=self.state
        )

    def add(
            self,
            req: define.user.AddUserReq
    ):
        t_user = self.dao.table["user"]
        t_password = self.dao.table["password"]
        t_user_dept = self.dao.table["user_dept"]
        user_data = req.user_data()
        password_data = req.password_data()
        dept_data = req.dept_data()
        with self.state.dao.trans() as tx:
            if user_data:
                self.state.dao.execute(
                    self.state.dao.insert(
                        t_user, update=req.update
                    ).values(user_data),
                    tx=tx,
                )
            if password_data:
                self.state.dao.execute(
                    self.state.dao.insert(
                        t_password, update=req.update
                    ).values(password_data),
                    tx=tx,
                )
            if dept_data:
                self.state.dao.execute(
                    self.state.dao.insert(
                        t_user_dept, update=req.update
                    ).values(dept_data),
                    tx=tx,
                )

    def set_(
            self,
            req: define.user.UserReq
    ):

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

