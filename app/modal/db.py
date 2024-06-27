from typing import Tuple, List, Dict, Any
import sqlalchemy as sa
from app import shared


__all__ = (
    "Dept",
    "User",
    "UserDept",
    "KlType",
    "KlDoc",
    "KlDetail",
)


class Table(object):

    __tablename__ = None

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
        name = name or cls.__tablename__
        t = dao.table.register(
            name, *cls.columns(),
        )
        return t


class Dept(Table):

    __tablename__ = "dept"

    def __init__(
            self,
            name: str | None = None,
    ):
        super().__init__(
            name=name
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

    __tablename__ = "user"

    def __init__(
            self,
            name: str | None = None,
    ):
        super().__init__(
            name=name
        )

    @classmethod
    def columns(cls):
        return (
            sa.Column("id", sa.BIGINT, nullable=False),
            sa.Column("user", sa.VARCHAR(512), nullable=False),
            sa.Column("name", sa.VARCHAR(512), nullable=False),
            sa.Column("order", sa.INT, nullable=False, default=0),
            sa.Column("create_by", sa.BIGINT, nullable=False, default=0),
            sa.Column("create_at", sa.INT, nullable=False, default=0),
            sa.PrimaryKeyConstraint("id")
        )


class Password(Table):

    __tablename__ = "password"

    def __init__(
            self,
            name: str | None = None,
    ):
        super().__init__(
            name=name
        )

    @classmethod
    def columns(cls):
        return (
            sa.Column("id", sa.BIGINT, nullable=False),
            sa.Column("password", sa.VARCHAR(512), nullable=False),
            sa.PrimaryKeyConstraint("id")
        )


class UserDept(Table):

    __tablename__ = "user_dept"

    def __init__(
            self,
            name: str | None = None,
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


class DocFolder(Table):

    __tablename__ = "doc_folder"

    def __init__(
            self,
            name: str | None = None,
    ):
        super().__init__(
            name=name
        )

    @classmethod
    def columns(cls):
        return (
            sa.Column("id", sa.BIGINT, nullable=False),
            sa.Column("pid", sa.BIGINT, nullable=False, default=0),
            sa.Column("name", sa.VARCHAR(512), nullable=False),
            sa.Column("create_by", sa.BIGINT, nullable=False, default=0),
            sa.Column("create_at", sa.BIGINT, nullable=False, default=0),
        )


class DocFile(Table):

    __tablename__ = "doc_file"

    def __init__(
            self,
            name: str | None = None,
    ):
        super().__init__(
            name=name
        )

    @classmethod
    def columns(cls):
        return (
            sa.Column("id", sa.BIGINT, nullable=False),
            sa.Column("pid", sa.BIGINT, nullable=False, default=0),
            sa.Column("name", sa.VARCHAR(512), nullable=False),
            sa.Column("ext", sa.VARCHAR(16), nullable=False),
            sa.Column("md5", sa.VARCHAR(512), nullable=False),
            sa.Column("create_by", sa.BIGINT, nullable=False, default=0),
            sa.Column("create_at", sa.BIGINT, nullable=False, default=0),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("md5"),
        )


class KlType(Table):

    __tablename__ = "kl_type"

    def __init__(
            self,
            name: str | None = None,
    ):
        super().__init__(
            name=name
        )

    @classmethod
    def columns(cls):
        return (
            sa.Column("id", sa.BIGINT, nullable=False),
            sa.Column("pid", sa.BIGINT, nullable=False, default=0),
            sa.Column("collection", sa.VARCHAR(512), nullable=False, default=""),
            sa.Column("name", sa.VARCHAR(1024), nullable=False),
            sa.Column("create_by", sa.BIGINT, nullable=False, default=0),
            sa.Column("create_at", sa.INT, nullable=False, default=0),
            sa.PrimaryKeyConstraint("id")
        )


class KlDoc(Table):

    __tablename__ = "kl_doc"

    def __init__(
            self,
            name: str | None = None,
    ):
        super().__init__(
            name=name
        )

    @classmethod
    def columns(cls):
        return (
            sa.Column("id", sa.BIGINT, nullable=False),
            sa.Column("pid", sa.BIGINT, nullable=False),
            sa.Column("name", sa.VARCHAR(1024), nullable=False),
            sa.Column("ext", sa.VARCHAR(32), nullable=False),
            sa.Column("create_by", sa.BIGINT, nullable=False, default=0),
            sa.Column("create_at", sa.INT, nullable=False, default=0),
            sa.PrimaryKeyConstraint("id"),
        )


class KlDetail(Table):

    __tablename__ = "kl_detail"

    def __init__(
            self,
            name: str | None = None,
    ):
        super().__init__(
            name=name
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

    __tablename__ = "chat_log"

    def __init__(
            self,
            name: str | None = None,
    ):
        super().__init__(
            name=name
        )

    @classmethod
    def columns(cls):
        return (
            sa.Column("id", sa.BIGINT, nullable=False, default=0),
            sa.Column("pid", sa.BIGINT, nullable=False, default=0),
            sa.Column("type", sa.INT, nullable=False, default=0),
            sa.Column("role", sa.VARCHAR(128), nullable=False, default=""),
            sa.Column("content", sa.TEXT, nullable=False, default=""),
            sa.Column("create_by", sa.BIGINT, nullable=False, default=0),
            sa.Column("create_at", sa.INT, nullable=False, default=0),
            sa.PrimaryKeyConstraint("id")
        )


