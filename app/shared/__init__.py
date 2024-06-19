from . import config
from . import dao
from . import embedding
from . import vector
from . import doc
from . import auth
from . import chat
from .img import img
from .router import router


config.load(
    config_path="./config/config.yaml"
)
