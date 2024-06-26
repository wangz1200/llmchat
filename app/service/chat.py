import json
import re

from .base import *
from .doc import doc as svc_doc


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

    def extract_knowledge_prompt(
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
            embedding=emb,
            output_fields=["id", "pid", "name", "ext", "text"]
        )
        keys = {}
        text = []
        reference = []
        for c in context:
            c = c["entity"]
            text.append(c["text"])
            if c["id"] not in keys:
                reference.append({
                    "id": c["id"],
                    "pid": c["pid"],
                    "ext": c["ext"],
                    "name": c["name"],
                })
        if not text:
            return "", []
        return text, reference

    def prepare_function_prompt(
            self
    ):
        pass

    async def chat(
            self,
            req: define.chat.ChatReq,
    ):
        model = req.model or self.model
        temperature = req.temperature or self.temperature
        max_tokens = req.max_tokens or self.max_tokens
        messages = req.messages
        if not isinstance(messages, list):
            messages = [messages, ]
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
            }, ensure_ascii=False)

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
        reference = []
        if req.knowledge:
            first = messages[0]
            last = messages[-1]
            query = last["content"]
            text, reference = self.extract_knowledge_prompt(
                query=query,
                knowledge=req.knowledge,
            )
            system_prompt = self.KL_PROMPT_TEMPLATE.format(
                context="\n\n".join(text),
            )
            if first["role"] != "system":
                messages = [{"role": "system", "content": system_prompt}, ] + messages
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
        yield json.dumps({
            "reference": reference,
        }, ensure_ascii=False)

    async def func_call(
            self,
            query: str,
    ):
        function_pattern = r"<\|FUNCTION\|>: (.*?)\n"
        args_pattern = r"<\|ARGS\|>: (.*)"
        template = modal.tool.function.template()
        messages = [
            {
                "role": "system",
                "content": template
            },
            {
                "role": "user",
                "content": query,
            }
        ]
        text = state.llm.chat.completions.create(
            messages=messages,
            model=self.model,
            max_tokens=self.max_tokens,
            stream=True,
            temperature=0,
            stop=["<|RETURN|>", "<|im_end|>", "<|endoftext|>", ],
        )
        context = ""
        ret = []
        for t in text:
            c = t.choices[0].delta.content
            if not c:
                continue
            context += c
        fn_match = re.search(function_pattern, context)
        names = fn_match.group(1)
        args_match = re.search(args_pattern, context)
        args = args_match.group(1)
        names = names.split(",")
        for name in names:
            name = name.strip()
            fn = getattr(modal.tool.function, name)
            a = json.loads(args)
            if not fn:
                continue
            ret.append(fn(a))
        return ret

    async def tool(
            self,
            req: define.chat.ChatToolReq,
    ):
        messages = shared.util.list_(req.messages)
        last = messages[-1]
        ret = await self.func_call(
            query=last["content"]
        )
        system = []
        if ret:
            prompt = "\n".join(ret)
            system = {
                "role": "system",
                "content": prompt,
            }
        if len(messages) == 1 and system:
            messages = [system, ] + messages
        text = state.llm.chat.completions.create(
            messages=messages,
            model=req.model or self.model,
            max_tokens=req.max_tokens or self.max_tokens,
            stream=True,
            temperature=req.temperature or self.temperature,
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
            }, ensure_ascii=False)


chat = Chat(
    state=state,
    model=shared.config.args["llm"]["model"],
    max_tokens=shared.config.args["llm"]["max_tokens"],
)
