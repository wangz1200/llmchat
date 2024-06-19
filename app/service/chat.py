import openai
from .base import *


llm = openai.OpenAI(
    base_url="http://10.133.95.100:9103/v1",
    api_key="None",
)


async def chat(
        messages: List[Dict[str, str]],
        system: str | None = None,
        model: str = "llm",
        max_tokens: int = 8192,
        temperature: float = 0.0,
):
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
        yield {
            "role": "assistant",
            "content": c,
        }


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

