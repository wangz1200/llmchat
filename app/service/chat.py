import json
from .base import *


__all__ = (
    "chat",
)


class Chat(object):

    def __init__(
            self,
            model: str | None = None,
            max_tokens: int | None = None,
            temperature: float = 0,
    ):
        super(Chat, self).__init__()
        self.model = model or "default"
        self.temperature = temperature or 0.00
        self.max_tokens = max_tokens or 4096

    def _preprocess(
            self,
            messages: List[Dict[str, str]],
    ):
        if not messages:
            return messages
        first = messages[0]
        if first["role"] != "system":
            system = {
                "role": "system",
                "content": "You are a assistant"
            }
            messages = [system] + messages
        return messages

    async def chat_function(
            self,
            prompt: str,
    ):
        pass

    def prepare_kl_system_prompt(
            self,
            query: str,
            knowledge: str,
    ):
        if not isinstance(query, list):
            query = [query, ]
        emb = self.state.embedding(query)

    async def chat(
            self,
            messages: List[Dict[str, str]],
            sid: str | int = 0,
            model: str | None = None,
            max_tokens: int | None = None,
            temperature: float = 0.0,
            knowledge: str | None = None,
    ):
        model = model or self.model
        temperature = temperature or self.temperature
        max_tokens = max_tokens or self.max_tokens
        text = state.llm.chat.completions.create(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            stream=True,
            temperature=temperature,
            stop=["<|im_end|>", "<|endoftext|>", ],
        )
        id_ = shared.snow.sid()
        for i, t in enumerate(text):
            c = t.choices[0].delta.content
            if not c:
                continue
            yield json.dumps({
                "id": id_,
                "sid": sid,
                "index": i,
                "role": "assistant",
                "content": c,
            }, ensure_ascii=False)


chat = Chat(
    model=shared.config.args["llm"]["model"],
    max_tokens=shared.config.args["llm"]["max_tokens"],
)
