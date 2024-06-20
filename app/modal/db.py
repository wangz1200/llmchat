from typing import Tuple, List, Dict, Any
import sqlalchemy as sa
from app import shared


__all__ = (
    "Dept",
    "User",
    "UserDept",
    "KDType",
    "KDDoc",
    "KDDetail",
)


class Table(object):

    def __init__(
            self,
            name: str,
    ):
        self.name = name

    @classmethod
    def columns(cls):
        raise NotImplementedError

    @classmethod
    def register(
            cls,
            dao: shared.dao.DAO,
            name: str | None = None,
    ):
        m = cls(name=name)
        t = dao.table.register(
            m.name, *m.columns(),
        )
        return t


class Dept(Table):

    def __init__(
            self,
            name: str | None = None,
    ):
        super().__init__(
            name=name or "dept"
        )

    @classmethod
    def columns(cls):
        return (
            sa.Column("id", sa.BIGINT, nullable=False),
            sa.Column("pid", sa.BIGINT, nullable=False, default=0),
            sa.Column("name", sa.VARCHAR(512), nullable=False),
            sa.Column("order", sa.INT, nullable=False, default=0),
            sa.Column("create_at", sa.INT, nullable=False, default=0),
            sa.PrimaryKeyConstraint("id")
        )


class User(Table):

    def __init__(
            self,
            name: str | None = "user",
    ):
        super().__init__(
            name=name or "user"
        )

    @classmethod
    def columns(cls):
        return (
            sa.Column("id", sa.BIGINT, nullable=False),
            sa.Column("user", sa.VARCHAR(512), nullable=False),
            sa.Column("name", sa.VARCHAR(512), nullable=False),
            sa.Column("dept", sa.BIGINT, nullable=False, default=0),
            sa.Column("order", sa.INT, nullable=False, default=0),
            sa.Column("create_by", sa.BIGINT, nullable=False, default=0),
            sa.Column("create_at", sa.INT, nullable=False, default=0),
            sa.PrimaryKeyConstraint("id")
        )


class UserDept(Table):

    def __init__(
            self,
            name: str | None = "user_dept",
    ):
        super().__init__(
            name=name
        )

    @classmethod
    def columns(cls):
        return (
            sa.Column("user", sa.BIGINT, nullable=False),
            sa.Column("dept", sa.BIGINT, nullable=False),
            sa.UniqueConstraint("user", "dept"),
        )


class KDType(Table):

    def __init__(
            self,
            name: str | None = "kd_type",
    ):
        super().__init__(
            name=name or "kd_type",
        )

    @classmethod
    def columns(cls):
        return (
            sa.Column("id", sa.BIGINT, nullable=False),
            sa.Column("pid", sa.BIGINT, nullable=False, default=0),
            sa.Column("name", sa.VARCHAR(1024), nullable=False),
            sa.Column("create_by", sa.BIGINT, nullable=False, default=0),
            sa.Column("create_at", sa.INT, nullable=False, default=0),
            sa.PrimaryKeyConstraint("id")
        )


class KDDoc(Table):

    def __init__(
            self,
            name: str | None = "kd_doc",
    ):
        super().__init__(
            name=name or "kd_doc"
        )

    @classmethod
    def columns(cls):
        return (
            sa.Column("id", sa.BIGINT, nullable=False),
            sa.Column("title", sa.VARCHAR(512), nullable=False),
            sa.Column("name", sa.VARCHAR(1024), nullable=False),
            sa.Column("create_by", sa.BIGINT, nullable=False, default=0),
            sa.Column("create_at", sa.INT, nullable=False, default=0),
            sa.PrimaryKeyConstraint("id"),
        )


class KDDetail(Table):

    def __init__(
            self,
            name: str | None = "kd_detail"
    ):
        super().__init__(
            name=name or "kd_detail"
        )

    @classmethod
    def columns(cls):
        return (
            sa.Column("id", sa.BIGINT, nullable=False),
            sa.Column("pid", sa.BIGINT, nullable=False, default=0),
            sa.Column("keyword", sa.VARCHAR(1024), nullable=False, default=""),
            sa.Column("content", sa.TEXT, nullable=False),
            sa.Column("create_by", sa.BIGINT, nullable=False, default=0),
            sa.Column("create_at", sa.INT, nullable=False, default=0),
            sa.PrimaryKeyConstraint("id"),
        )


class ChatLog(Table):

    def __init__(
            self,
            name: str | None = "chat_log"
    ):
        super().__init__(
            name=name or "chat_log"
        )

    @classmethod
    def columns(cls):
        return (
            sa.Column("id", sa.BIGINT, nullable=False, default=0),
            sa.Column("pid", sa.BIGINT, nullable=False, default=0),
            sa.Column("type", sa.INT, nullable=False, default=0),
            sa.Column("role", sa.INT, nullable=False, default=0),
            sa.Column("content", sa.TEXT, nullable=False, default=""),
            sa.Column("create_by", sa.BIGINT, nullable=False, default=0),
            sa.Column("create_at", sa.INT, nullable=False, default=0),
            sa.PrimaryKeyConstraint("id")
        )


