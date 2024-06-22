import json
import os.path
from sentence_transformers import SentenceTransformer
from .base import *


__all__ = (
    "Embedding",
)


class Embedding(object):

    def __init__(
            self,
            model_name_or_path: str,
            device: str = "cuda",
            normalized: bool = False,
    ):
        super(Embedding, self).__init__()
        self.config = {}
        self.normalized = normalized
        self.m = SentenceTransformer(
            model_name_or_path=model_name_or_path,
            device=device,
        )
        config_path = os.path.join(
            model_name_or_path,
            "config.json"
        )
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf8") as f:
                self.config = json.load(f)

    @property
    def hidden_size(self):
        return self.config.get("hidden_size", -1)

    def encode(
            self,
            text: str | List[str],
            normalized: bool = False,
    ):
        text = (
            text if isinstance(text, list) else [text]
        )
        if not text:
            return []
        normalized = normalized or self.normalized
        embeddings = self.m.encode(
            sentences=text,
            normalize_embeddings=normalized
        )
        ret = [
            {"embedding": embed.tolist()} for embed in embeddings
        ]
        return ret
