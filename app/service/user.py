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

    def add(
            self,
            req: define.user.AddUserReq,
            tx: sa.Connection | None = None,
    ):
        data = req.password()
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
            req: define.user.SetUserReq,
            tx: sa.Connection | None = None,
    ):
        data = req.password()
        if not data:
            return
        t = self.dao.table["password"]
        for d in data:
            stmt = self.state.dao.update(t).values(d)
            self.state.dao.execute(
                stmt=stmt,
                tx=tx,
            )


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
            req: define.user.AddUserReq,
            tx: sa.Connection | None = None,
    ):
        data = req.dept()
        if not data:
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
            req: define.user.SetUserReq,
            tx: sa.Connection | None = None,
    ):
        data = req.dept()
        if not data:
            return
        t = self.dao.table["user_dept"]
        for d in data:
            stmt = self.state.dao.update(t).values(d)
            self.state.dao.execute(
                stmt=stmt,
                tx=tx,
            )


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
        with self.state.dao.trans() as tx:
            data = req.user()
            self.state.dao.execute(
                self.state.dao.insert(
                    table=self.dao.table["user"],
                    update=req.update
                ).values(data),
                tx=tx,
            )
            self.password.add(
                req=req,
                tx=tx,
            )
            self.dept.add(
                req=req,
                tx=tx,
            )

    def set_(
            self,
            req: define.user.SetUserReq
    ):
        with self.state.dao.trans() as tx:
            data = req.user()
            self.state.dao.execute(
                self.state.dao.update(
                    table=self.dao.table["user"],
                ).values(data),
                tx=tx,
            )
            self.password.set_(
                req=req,
                tx=tx,
            )
            self.dept.set_(
                req=req,
                tx=tx,
            )

    def exists(
            self,
            id_: str | int | List[int] | List[str],
    ):
        if isinstance(id_, str):
            id_ = id_.split(",")
        if not isinstance(id_, list):
            id_ = [id_, ]
        if not id_:
            raise ValueError("ID不能为空。")
        t = self.dao.table["user"]
        stmt = self.state.dao.select(
            sa.func.count(t.c.id)
        ).where(
            t.c.id.in_(id_)
        )
        count = self.state.dao.execute(stmt).scalar()
        return count == len(id_)


user = User(
    state=state
)

