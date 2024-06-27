from typing import Tuple, List, Dict, Any
from pathlib import Path
import openai
import sqlalchemy as sa
from app import shared, modal, define


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
    global state
    type_ = config["type"]
    if type_.lower() != "mysql":
        raise TypeError("Only MySQL is supported.")
    dao = shared.dao.MySQL(**config)
    state.dao = dao
    modal.db.Dept.register(dao)
    modal.db.User.register(dao)
    modal.db.Password.register(dao)
    modal.db.UserDept.register(dao)
    modal.db.DocFolder.register(dao)
    modal.db.DocFile.register(dao)
    # modal.db.KlType.register(dao)
    # modal.db.KlDoc.register(dao)
    # modal.db.KlDetail.register(dao)
    dao.table.create_all(
        checkfirst=True,
    )


def _init_vector(
        config: dict,
):
    global state
    type_ = config.get("type", None)
    if type_ != "milvus":
        raise TypeError("Only Milvus is supported.")
    host = config.get("host", "127.0.0.1")
    port = config.get("port", 19530)
    name = config.get("name", "default")
    if host and port:
        state.vector = shared.vector.Milvus(
            host=host,
            port=port,
            name=name,
        )
    else:
        raise ValueError("vector host and port must be specified.")


def _init_embedding(
        config: dict,
):
    global state
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
    global state
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

