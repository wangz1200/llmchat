from typing import List, Dict, Any
import datetime
import json5


__all__ = [
    "schema",
    "function",
]


FUNCTION_CALL_TEMPLATE = """
## 工具 | Tools
### 你拥有如下工具 | You have access to the following tools
{tools}
### 你可以在回复中插入零次、一次或多次以下命令以调用工具 | When you need to call a tool, please insert the following command in your reply, which can be called zero or multiple times according to your needs
<|FUNCTION|>: 工具名称，必须是[{names}]之一 | The tool to use, should be one of [{names}]。
<|ARGS|>: 工具输入 | The input of the tool
<|RESULT|>: 工具结果，需将图片用![](url)渲染出来 | The result returned by the tool. The image needs to be rendered as ![](url)
<|RETURN|>: 根据工具结果进行回复 | Reply based on tool result


"""


schema = [
    {
        "name": "get_current_datetime",
        "description": "获取当前日期 | Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": None,
            "required": None,
        },
    },
    {
        "name": "get_current_weather",
        "description": "根据位置获取当前天气 | Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "位置 | location",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                },
            },
            "required": ["location"],
        },
    },
]


class Function(object):

    def __init__(
            self,
            schema: List[Dict[str, Any]],
    ):
        super().__init__()
        self.schema = schema

    def function_json(self):
        return json5.dumps(
            self.schema,
            ensure_ascii=False,
        )

    def template(self):
        names = ",".join([f["name"] for f in self.schema])
        return FUNCTION_CALL_TEMPLATE.format(
            tools=self.function_json(),
            names=names
        )

    @staticmethod
    def get_current_datetime(
            kwargs,
    ):
        now = datetime.datetime.now()
        t = now.strftime("%Y年%m月%d日 %H时%M分%S秒")
        return f"当前时间为：{t}"

    @staticmethod
    def get_current_weather(
            location: str,
            unit: str,
    ):
        return f"""当前{location}气温为36摄氏度"""


function = Function(
    schema=schema,
)

