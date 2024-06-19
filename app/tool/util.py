from typing import Union

from .base import *
import pprint
import urllib.parse
import json5
from qwen_agent.agents import Assistant
from qwen_agent.tools.base import BaseTool, register_tool


__all__ = (
    "query_weather"
)


FUNCTION_DESC = [
    {
        "name": "query_weather",
        "description": "查询天气|query weather",
    }
]


def query_weather(
        location: str,
):
    return "天气晴朗"


@register_tool("query_weather")
class WeatherTool(BaseTool):

    description = "查询天气 | query weather"
    parameters = [{
        'name': 'prompt',
        'type': 'string',
        'description': '天气',
        'required': True
    }]

    def call(
            self,
            params: Union[str, dict],
            **kwargs,
    ) -> str:
        return json5.dumps({
            "weather": "晴，25℃",
        })


