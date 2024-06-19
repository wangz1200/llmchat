import json

import openai
from .base import *


base_url = shared.config.args["llm"]["url"]
api_key = shared.config.args["llm"]["key"]
MAX_TOKENS = shared.config.args["llm"]["max_tokens"]


llm = openai.OpenAI(
    base_url=base_url,
    api_key=api_key,
)


async def chat(
        messages: List[Dict[str, str]],
        system: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float = 0.0,
):
    model = model or shared.config.args["llm"]["model"]
    max_tokens = max_tokens or MAX_TOKENS
    text = llm.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        stop=["<|im_end|>", "<|endoftext|>", ],
    )
    for t in text:
        c = t.choices[0].delta.content
        if not c:
            continue
        yield json.dumps({
            "role": "assistant",
            "content": c,
        }, ensure_ascii=False)


async def chat_with_knowledge(
        knowledge: str,
        messages: List[Dict[str, str]],
        system: str | None = None,
        model: str = "llm",
        max_tokens: int = 8192,
        temperature: float = 0.0,
):
    return chat(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )

