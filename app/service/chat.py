import json
from .base import *

MAX_TOKENS = shared.config.args["llm"]["max_tokens"]


async def chat(
        messages: List[Dict[str, str]],
        system: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float = 0.0,
):
    model = model or shared.config.args["llm"]["model"]
    text = state.llm.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens or MAX_TOKENS,
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
        max_tokens: int | None = None,
        temperature: float = 0.0,
):
    max_tokens = max_tokens or MAX_TOKENS
    return chat(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )


async def chat_with_tools(
        messages: List[Dict[str, str]],
        tools: str | List[str],
        max_tokens: int | None = None,
        temperature: float = 0.0,
):
    if not messages:
        yield {
            "role": "assistant",
            "content": "信息不能为空",
        }


async def chat_with_agent():
    pass
