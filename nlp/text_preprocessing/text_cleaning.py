import re


def remove_noise(text):
    # 去除HTML标签
    text = re.sub(r'<.*?>', '', text)
    # 去除标点符号和特殊字符
    text = re.sub(r'[^\w\s]', '', text)
    return text


example_text = "<p>Hello, World! Here's a <a href='https://example.com'>link</a>.</p>"
clean_text = remove_noise(example_text)
print(clean_text)

# 全部标准化成小写
tokens_normalized = [token.lower() for token in clean_text]
print(tokens_normalized)
