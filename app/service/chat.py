import json
from .base import *

__all__ = (
    "chat",
)


class _Logger(object):

    def __init__(
            self,
            state: State | None = None
    ):
        super().__init__()
        self.state = state

    def record(
            self,
            data: Dict | List[Dict],
            update: bool | None = None,
    ):
        t_chat_log = self.state.dao.table["chat_log"]
        stmt = self.state.dao.insert(
            t_chat_log, update=update,
        ).values(data)
        self.state.dao.insert(stmt)

    def list_(
            self,
            page_no: int | None = None,
            page_size: int | None = None,
    ):
        page_no = page_no or 1
        page_size = page_size or 30
        t_chat_log = self.state.dao.table["chat_log"]
        stmt = self.state.dao.select(
            t_chat_log
        ).limit(
            page_size
        ).offset(
            (page_no - 1) * page_size
        )
        rows = self.state.dao.execute(stmt)
        rows = self.state.dao.list_(rows)
        return rows

    def delete(
            self,
    ):
        pass


class Chat(object):
    KL_PROMPT_TEMPLATE = """
根据以下文内容进行专业对话。
<内容>
{context}
</内容>


"""
    FUNC_PROMPT_TEMPLATE = """
"""

    def __init__(
            self,
            state: State | None = None,
            model: str | None = None,
            max_tokens: int | None = None,
            temperature: float = 0,
    ):
        super(Chat, self).__init__()
        self.state = state
        self.model = model or "default"
        self.temperature = temperature or 0.00
        self.max_tokens = max_tokens or 4096
        self.logger = _Logger(state=self.state)

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

    def prepare_knowledge_prompt(
            self,
            query: str,
            knowledge: str,
    ):
        if not isinstance(query, list):
            query = [query, ]
        emb = self.state.embedding.encode(query)
        emb = [e["embedding"] for e in emb]
        context = self.state.vector.search(
            name=knowledge,
            embedding=emb
        )
        text = [
            c["entity"]["text"]
            for c in context
        ]
        if not text:
            return ""
        prompt = self.KL_PROMPT_TEMPLATE.format(
            context="\n\n".join(text),
        )
        return prompt

    def prepare_function_prompt(
            self
    ):
        pass

    async def chat(
            self,
            messages: List[Dict[str, str]],
            pid: str | int = 0,
            model: str | None = None,
            max_tokens: int | None = None,
            stream: bool = True,
            temperature: float = 0.0,
            knowledge: str | None = None,
            log: bool = False,
    ):
        model = model or self.model
        temperature = temperature or self.temperature
        max_tokens = max_tokens or self.max_tokens
        if knowledge:
            first = messages[0]
            last = messages[-1]
            query = last["content"]
            prompt = self.prepare_kl_prompt(
                query=query,
                knowledge=knowledge,
            )
            if first["role"] != "system":
                messages = [{"role": "system", "content": query}, ] + messages
            else:
                first["content"] = prompt
        text = state.llm.chat.completions.create(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            stream=True,
            temperature=temperature,
            stop=["<|im_end|>", "<|endoftext|>", ],
        )
        id_ = shared.snow.sid()
        idx = 0
        all_ = ""
        for t in text:
            idx += 1
            c = t.choices[0].delta.content
            if not c:
                continue
            if stream:
                yield json.dumps({
                    "id": id_,
                    "pid": pid,
                    "index": idx,
                    "role": "assistant",
                    "content": c,
                }, ensure_ascii=False)
            if not stream or log:
                all_ += c
        if log:
            data = [
                {
                    "id": id_,
                    "pid": pid,
                    "role": messages[-1]["role"],
                    "content": messages[-1]["content"],
                    "create_by": 0,
                    "create_at": 0,
                },
                {
                    "id": id_,
                    "pid": pid,
                    "role": "assistant",
                    "content": all_,
                    "create_by": 0,
                    "create_at": 0,
                }
            ]
            self.logger.record(
                data=data,
                update=True,
            )
        if not stream:
            yield {
                "id": id_,
                "pid": pid,
                "index": idx,
                "role": "assistant",
                "content": all_,
            }

    async def knowledge(
            self,
            req: define.chat.ChatReq,
    ):
        model = req.model or self.model
        temperature = req.temperature or self.temperature
        max_tokens = req.max_tokens or self.max_tokens
        messages = req.messages
        if not isinstance(messages, list):
            messages = [messages, ]
        if req.knowledge:
            first = messages[0]
            last = messages[-1]
            query = last["content"]
            prompt = self.prepare_knowledge_prompt(
                query=query,
                knowledge=req.knowledge,
            )
            if first["role"] != "system":
                messages = [{"role": "system", "content": prompt}, ] + messages
        text = state.llm.chat.completions.create(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            stream=True,
            temperature=temperature,
            stop=["<|im_end|>", "<|endoftext|>", ],
        )
        id_ = shared.snow.sid()
        idx = 0
        all_ = ""
        for t in text:
            c = t.choices[0].delta.content
            if not c:
                continue
            if req.stream:
                idx += 1
                yield json.dumps({
                    "id": id_,
                    "pid": req.pid,
                    "index": idx,
                    "role": "assistant",
                    "content": c,
                }, ensure_ascii=False)
            if not req.stream or req.log:
                all_ += c
        if req.log:
            data = [
                {
                    "id": id_,
                    "pid": req.pid,
                    "role": messages[-1]["role"],
                    "content": messages[-1]["content"],
                    "create_by": 0,
                    "create_at": 0,
                },
                {
                    "id": id_,
                    "pid": req.pid,
                    "role": "assistant",
                    "content": all_,
                    "create_by": 0,
                    "create_at": 0,
                }
            ]
            self.logger.record(
                data=data,
                update=True,
            )
        if not req.stream:
            yield json.dumps({
                "id": id_,
                "pid": req.pid,
                "index": idx,
                "role": "assistant",
                "content": all_,
            }, ensure_ascii=False, )


chat = Chat(
    state=state,
    model=shared.config.args["llm"]["model"],
    max_tokens=shared.config.args["llm"]["max_tokens"],
)
