from .base import *
from sentence_transformers import SentenceTransformer


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
        self.normalized = normalized
        self.m = SentenceTransformer(
            model_name_or_path=model_name_or_path,
            device=device,
        )

    def encode(
            self,
            text: str | List[str],
            normalized: bool = False,
    ):
        text = (
            text if isinstance(text, list) else [text]
        )
        normalized = normalized or self.normalized
        embeddings = self.m.encode(
            sentences=text,
            normalize_embeddings=normalized
        )
        ret = [
            {"embedding": embed.tolist()} for embed in embeddings
        ]
        return ret

    def __call__(
            self,
            text: str | List[str],
    ):
        return self.encode(
            text=text,
        )
