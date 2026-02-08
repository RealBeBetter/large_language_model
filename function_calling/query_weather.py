import inspect
import os
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
    params = {"city": city, }

    # 发送GET请求
    rsp = requests.get(url=url, params=params)
    # 检查响应状态
    if rsp.status_code == 200:
        # 解析响应数据
        data = rsp.json()
        return data

    return dict()


def gen_function_schema_by_llm() -> str:
    # 使用 inspect 模块提取文档字符串
    function_declaration = inspect.getdoc(query_weather)
    print(function_declaration)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system",
             "content": "你是一位优秀的数据分析师，现在有一个函数的详细声明如下：%s" % function_declaration},
            {"role": "user", "content": "请根据这个函数声明，为我生成一个JSON Schema对象描述。这个描述应该清晰地标明函数的输入和输出规范。具体要求如下：\
                                 1. 在JSON Schema对象中，设置函数的参数类型为object'.\
                                 2. 'properties字段如果有参数，必须表示出字段的描述. \
                                 3. 从函数声明中解析出函数的描述，并在JSON Schema中以中文字符形式表示在'description'字段.\
                                 4. 识别函数声明中哪些参数是必需的，然后在JSON Schema的'required'字段中列出这些参数. \
                                 5. 输出的应仅为符合上述要求的JSON Schema对象内容,不需要任何上下文修饰语句. "}
        ]
    )

    content = response.choices[0].message.content
    print(content)
    return content


def llm_chat(city: str = "Shenzhen"):
    weather = query_weather(city)

    rsp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system",
             "content": "这是当前深圳市的实时天气数据：%s, 来源于 uapis 网站的 API：https://uapis.cn/api/v1/misc/weather" % weather},
            {"role": "user", "content": "请问：当前深圳市的天气如何？"}
        ],
        stream=False
    )

    print(rsp.choices[0].message.content)


if __name__ == "__main__":
    # gen_function_schema_by_llm()
    llm_chat("Shenzhen")
