from typing import Tuple, List, Dict, Any
import openai
from app import shared


class State(object):

    def __init__(
            self,
            dao: shared.dao.DAO | None = None,
            vector: shared.vector.Milvus | None = None,
            embedding: shared.embedding.Embedding | None = None,
            llm: openai.OpenAI | None = None
    ):
        super().__init__()
        self.dao = dao
        self.vector = vector
        self.embedding = embedding
        self.llm = llm


state = State()


def _init_db(
        config: dict,
):
    from app import modal as M
    type_ = config["type"]
    if type_ != "mysql":
        raise TypeError("Only MySQL is supported.")
    dao = shared.dao.MySQL(**config)
    state.dao = dao
    M.db.Dept.register(dao)
    M.db.User.register(dao)
    M.db.UserDept.register(dao)
    M.db.KDType.register(dao)
    M.db.KDType.register(dao)
    M.db.KDDetail.register(dao)
    dao.table.create_all(
        checkfirst=True,
    )


def _init_vector(
        config: dict,
):
    type_ = config.get("type", None)
    if type_ != "milvus":
        raise TypeError("Only Milvus is supported.")
    host = config.get("host", None)
    port = config.get("port", None)
    if host and port:
        state.vector = shared.vector.Milvus(
            host=host,
            port=port,
        )
    else:
        raise ValueError("vector host and port must be specified.")


def _init_embedding(
        config: dict,
):
    type_ = config.get("type", None)
    if type_ != "local":
        raise TypeError("Embedding only local is supported.")
    name = config.get("name", None)
    if not name:
        raise ValueError("name must be specified.")
    name = f"./public/models/{name}"
    use_gpu = config.get("use_gpu", False)
    device = config.get("device", 0)
    device = f"cuda:{device}" if use_gpu else "cpu"
    normalized = config.get("normalized", False)
    embedding = shared.embedding.Embedding(
        model_name_or_path=name,
        device=device,
        normalized=normalized
    )
    state.embedding = embedding


def _init_llm(
        config: dict,
):
    base_url = config["url"]
    api_key = config["key"]
    state.llm = openai.OpenAI(
        base_url=base_url,
        api_key=api_key,
    )


def init():
    _init_db(shared.config.args["database"])
    _init_vector(shared.config.args["vector"])
    _init_embedding(shared.config.args["embedding"])
    _init_llm(shared.config.args["llm"])

