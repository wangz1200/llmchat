from typing import List, Dict
import re
import requests
import json


function_pattern = r'<\|FUNCTION\|>: (.*?)\n'
args_pattern = r'<\|ARGS\|>: (.*)'


def get_current_weather(
        location: str,
        unit: str
) -> str:
    return f"{location}天气为25摄氏度"


FUNCTIONS = {
    "get_current_weather": get_current_weather,
}


def listen_to_sse(
        url: str,
        messages: List[Dict[str, str]],
):
    response = requests.post(
        url=url,
        stream=True,
        json={
            "messages": messages,
        }
    )
    ret = ""
    for line in response.iter_lines():
        if line:
            data = line.decode('utf-8').replace("data: ", "")
            data = json.loads(data)
            ret += data["content"]
    # print("------")
    # print(ret)
    # function_match = re.search(function_pattern, ret)
    # args_match = re.search(args_pattern, ret)
    # function_result = function_match.group(1) if function_match else None
    # args_result = args_match.group(1) if args_match else None
    # if function_result not in FUNCTIONS:
    #     raise Exception
    # func = FUNCTIONS.get(function_result)
    # args = json.loads(args_result)
    # ret = func(**args)
    print(ret)


if __name__ == "__main__":
    system_content_1 = """
You are a helpful assistant.
# Tools
## 你可以访问以下工具:
### get_current_weather
get_current_weather: 根据位置获取天气 | Get the current weather in a given location
参数: {"type": "object", "properties": {"location": {"type": "string", "description": "位置 | The city and state, e.g. San Francisco, CA"}, "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}}, "required": ["location"]}
## 当你要调用工具时，请在回复中插入以下命令，可根据需要调用零或多次: | When you need to call a tool, please insert the following command in your reply, which can be called zero or multiple times according to your needs:
<|FUNCTION|>: 要使用的工具，在[get_current_weather]中选择。
<|ARGS|>: 工具参数
<|RESULT|>: 结果
<|RETURN|>: 结束
"""
    system_content_2 = """
You are a helpful assistant.
# Tools
## 你可以访问以下工具:
### get_current_weather
get_current_weather: 根据位置获取天气 | Get the current weather in a given location
参数: {"type": "object", "properties": {"location": {"type": "string", "description": "位置 | The city and state, e.g. San Francisco, CA"}, "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}}, "required": ["location"]}
## 当你要调用工具时，请在回复中插入以下命令，可根据需要调用零或多次: | When you need to call a tool, please insert the following command in your reply, which can be called zero or multiple times according to your needs:
<|FUNCTION|>: 要使用的工具，在[get_current_weather]中选择。
<|ARGS|>: {"location": "北京"}
<|RESULT|>: None
<|RETURN|>: None
"""
    system_3 = """
调用获取天气函数get_current_weather返回如下结果：
{"location": "北京", "unit": "celsius", "temperature": 36}
    """
    url = "http://127.0.0.1:9000/chat"
    listen_to_sse(
        url=url,
        messages=[
            {
              "role": "system",
              "content": system_3
            },
            {
                "role": "user",
                "content": "查询北京天气"
            },
        ]
    )

    pass

