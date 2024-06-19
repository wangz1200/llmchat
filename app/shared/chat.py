from .base import *
import openai


class ChatOpenAI(object):

    def __init__(
            self,
            model: str,
            url: str,
            key: str | None = None,
    ):
        super().__init__()
        self.model = model
        self.client = openai.OpenAI(
            base_url=url,
            api_key=key or "None",
        )

    async def chat(
            self,
            messages: str | Dict[str, str],
            stream: bool = True,
    ):
        pass
