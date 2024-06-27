import re


function_pattern = r"<\|FUNCTION\|>: (.*?)\n"
args_pattern = r"<\|ARGS\|>: (.*)"


if __name__ == "__main__":
    names = "get_current_datetime, get_current_weather"
    ret = f"""
<|FUNCTION|>: {names}
<|ARGS|>: 123
<|RESULT|>: 工具结果，需将图片用![](url)渲染出来 | The result returned by the tool. The image needs to be rendered as ![](url)
<|RETURN|>: 根据工具结果进行回复 | Reply based on tool result
"""
    function_match = re.search(function_pattern, ret)
    args_match = re.search(args_pattern, ret)
    function_result = function_match.group(1)

    pass


