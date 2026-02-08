import json
import os
from typing import List, Dict

import requests
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")


def query_weather(city: str = "Beijing") -> dict:
    """
    :param city: 查询的城市名称，简体中文拼音
    :return: 该城市的天气信息，JSON 结构
    """

    # 构建请求URL
    url = "https://uapis.cn/api/v1/misc/weather"

    # 查询的城市，默认为北京
    params = {"city": city}

    # 发送GET请求
    rsp = requests.get(url=url, params=params)
    # 检查响应状态
    if rsp.status_code == 200:
        # 解析响应数据
        data = rsp.json()
        return data

    return dict()


def get_functions() -> list:
    # 构建函数的 JSON Schema 描述
    function_schema = {
        "type": "function",
        "function": {
            "name": "query_weather",
            "description": "获取指定城市的实时天气信息，包括温度、天气状况等",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，支持简体中文拼音格式，如：beijing 或 shenzhen"
                    }
                },
                "required": ["city"],
                "additionalProperties": False
            }
        }
    }

    # 返回函数列表
    return [function_schema]


def chat_with_fn_calling(messages: List[Dict]) -> Dict:
    """
    使用Function Calling进行聊天

    Args:
        messages: 消息历史列表

    Returns:
        Dict: 模型响应消息
    """
    tools = get_functions()

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        return response.choices[0].message
    except Exception as e:
        print(f"API调用异常: {str(e)}")
        return {"content": "抱歉，服务暂时不可用", "tool_calls": None}


def process_tool_calls(message: Dict, messages: List[Dict]) -> bool:
    """
    处理工具调用并更新消息历史

    Args:
        message: 模型响应消息
        messages: 消息历史列表

    Returns:
        bool: 是否处理了工具调用
    """
    if not hasattr(message, 'tool_calls') or not message.tool_calls:
        return False

    # 添加助理的消息到历史
    assistant_msg = {
        "role": "assistant",
        "content": message.content or "",
        "tool_calls": [
            {
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments
                }
            } for tool_call in message.tool_calls
        ]
    }
    messages.append(assistant_msg)

    # 处理每个工具调用
    for tool_call in message.tool_calls:
        func_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print(f"🔄 检测到工具调用: {func_name}, 参数: {arguments}")

        if func_name == "query_weather":
            city = arguments.get("city", "Beijing")
            weather_result = query_weather(city)

            # 将工具执行结果添加到消息历史
            tool_msg = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(weather_result, ensure_ascii=False)
            }
            messages.append(tool_msg)
            print(f"✅ 天气查询完成: {city}")

        else:
            # 处理未知函数
            error_msg = {"error": f"未知函数: {func_name}"}
            tool_msg = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(error_msg)
            }
            messages.append(tool_msg)
            print(f"❌ 未知函数: {func_name}")

    return True


def llm_chat(user_input: str = "请告诉我现在深圳的天气如何？", max_iterations: int = 3) -> None:
    """
    主要的LLM聊天函数，支持Function Calling

    Args:
        user_input: 用户输入
        max_iterations: 最大迭代次数，防止无限循环
    """
    # 初始化消息历史
    messages = [{"role": "user", "content": user_input}]

    iteration = 0
    while iteration < max_iterations:
        iteration += 1
        print(f"\n=== 第{iteration}轮对话 ===")

        # 调用模型
        rsp_msg = chat_with_fn_calling(messages)

        # 检查是否需要工具调用
        if process_tool_calls(rsp_msg, messages):
            # 如果处理了工具调用，继续下一轮迭代
            print("🔄 工具调用处理完成，继续生成回复...")
            continue
        else:
            # 没有工具调用，显示最终回复
            if hasattr(rsp_msg, 'content') and rsp_msg.content:
                print(f"🤖 AI回复: {rsp_msg.content}")
            else:
                print("❌ 模型未返回有效回复")
            break
    else:
        print("⚠️ 达到最大迭代次数，对话结束")


if __name__ == "__main__":
    test_queries = [
        # "今天北京的天气怎么样？",
        # "上海和北京的天气对比",
        # "帮我看看广州的天气",
        "查询深圳的天气情况",
    ]

    for query in test_queries:
        print(f"\n用户查询: {query}")
        llm_chat(query)
