import sqlalchemy as sa


__all__ = (
    "DAO",
    "MySQL",
)


class Table(object):

    def __init__(
            self,
            engine: sa.Engine,
            metadata: sa.MetaData,
    ):
        super(Table, self).__init__()
        self.engine = engine
        self.metadata = metadata

    def register(
            self,
            name: str,
            *columns,
            **kwargs,
    ):
        t = sa.Table(
            name, self.metadata,
            *columns,
            **kwargs,
        )
        return t

    def create(
            self,
            name: str,
            columns: list,
            **kwargs,
    ):
        checkfirst = kwargs.pop("checkfirst", True)
        t = sa.Table(
            name, self.metadata,
            *columns,
            **kwargs,
        )
        t.create(
            bind=self.engine,
            checkfirst=checkfirst,
        )
        return t

    def create_all(
            self,
            **kwargs,
    ):
        checkfirst = kwargs.get("checkfirst", True)
        self.metadata.create_all(
            self.engine,
            checkfirst=checkfirst
        )

    def drop_all(self):
        pass

    def __getitem__(self, item):
        return self.metadata.tables.get(item, None)


class DAO(object):

    def __init__(
            self,
            driver: str,
            host: str,
            port: int | str,
            user: str,
            password: str,
            name: str,
            **kwargs
    ):
        super(DAO, self).__init__(**kwargs)
        self._url = sa.URL.create(
            drivername=driver,
            host=host,
            port=port,
            username=user,
            password=password,
            database=name,
            **kwargs,
        )
        self.engine: sa.Engine = sa.create_engine(self._url)
        self.metadata = sa.MetaData()
        self.table = Table(
            engine=self.engine,
            metadata=self.metadata,
        )
        self.select = sa.select
        self.insert = sa.insert
        self.update = sa.update
        self.delete = sa.delete

    def connect(self):
        return self.engine.connect()

    def trans(self):
        return self.engine.begin()

    def begin(self):
        return self.engine.begin()

    def execute(self, stmt, *args, **kwargs):
        with self.trans() as tx:
            return tx.execute(stmt, *args, **kwargs)

    @classmethod
    def list_(
            cls,
            rows: sa.engine.CursorResult,
            handler=None,
    ):
        keys = rows.keys()
        ret = []
        for row in rows:
            row = handler(row) if handler else dict(zip(keys, row))
            ret.append(row)
        return ret

    @classmethod
    def tree_(
            cls,
            rows: list,
            pid: str | int = 0,
    ):
        ret = []
        dict_ = {}
        for row in rows:
            dict_[row["id"]] = row
        for k, v in dict_.items():
            p = v["pid"]
            if p == str(pid) or p == int(pid):
                ret.append(v)
            else:
                dict_[p]["children"].append(v)
        return ret


def _mysql_insert(
        table: sa.Table,
        update: bool | None = None,
        expected: list | None = None,
):
    from sqlalchemy.dialects.mysql import insert as _insert
    stmt = _insert(table)
    if update is True:
        expected = expected or []
        on_update = {
            c.name: getattr(stmt.inserted, c.name)
            for c in stmt.inserted
            if c.name not in expected
        }
        if len(on_update) > 0:
            stmt = stmt.on_duplicate_key_update(on_update)
    elif update is False:
        stmt = stmt.prefix_with(" IGNORE")
    return stmt


class MySQL(DAO):

    def __init__(
            self,
            host="127.0.0.1",
            port=3306,
            user="root",
            password="root",
            name="default",
            **kwargs,
    ):
        super(MySQL, self).__init__(
            driver="mysql+pymysql",
            host=host,
            port=port,
            user=user,
            password=password,
            name=name,
            **kwargs,
        )
        self.insert = _mysql_insert
