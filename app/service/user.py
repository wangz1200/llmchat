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

    def add(
            self,
            req: define.user.AddUserReq,
            tx: sa.Connection | None = None,
    ):
        data = req.password()
        if not data:
            return
        t = self.state.dao.table["password"]
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
        t = self.state.dao.table["password"]
        stmt = self.state.dao.update(t)
        for d in data:
            id_ = d.pop("id", None)
            if not id_ or not d:
                continue
            self.state.dao.execute(
                stmt=stmt.values(**d).where(t.c.id == id_),
                tx=tx,
            )


class _Dept(object):

    def __init__(
            self,
            state: State = state,
    ):
        super().__init__()
        self.state = state

    def add(
            self,
            req: define.user.AddUserReq,
            tx: sa.Connection | None = None,
    ):
        data = req.dept()
        if not data:
            return
        t = self.state.dao.table["user_dept"]
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
        t = self.state.dao.table["user_dept"]
        stmt = self.state.dao.update(t)
        for d in data:
            id_ = d.pop("user", None)
            if not id_ or not d:
                continue
            self.state.dao.execute(
                stmt=stmt.values(**d).where(t.c.user == id_),
                tx=tx,
            )


class User(object):

    def __init__(
            self,
            state: State = state
    ):
        super().__init__()
        self.state = state
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
                    table=self.state.dao.table["user"],
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
            t = self.state.dao.table["user"]
            stmt = self.state.dao.update(t)
            for d in data:
                id_ = d.pop("id", None)
                if not id_ or not d:
                    continue
                self.state.dao.execute(
                    stmt=stmt.values(**d).where(t.c.id == id_),
                    tx=tx
                )
            self.password.set_(
                req=req,
                tx=tx,
            )
            self.dept.set_(
                req=req,
                tx=tx,
            )

    def delete(
            self,
            id_: str | int | List[str] | List[int] | None = None,
    ):
        if isinstance(id_, str):
            id_ = id_.split(",")
        if not isinstance(id_, list):
            id_ = [id_]
        if not id_:
            raise ValueError("用户ID不能为空")
        with self.state.dao.trans() as tx:
            t = self.state.dao.table["user"]
            stmt = self.state.dao.delete(t).where(
                t.c.id.in_(id_)
            )
            self.state.dao.execute(
                stmt=stmt, tx=tx,
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
        t = self.state.dao.table["user"]
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

