import re

import nltk
from nltk.corpus import stopwords

# Download the necessary NLTK resources
nltk.download('stopwords')


def remove_noise(text):
    # 去除HTML标签
    text = re.sub(r'<.*?>', '', text)
    # 去除标点符号和特殊字符
    text = re.sub(r'[^\w\s]', '', text)
    return text


stop_words = set(stopwords.words('english'))  # 获取英文停用词列表
print(stop_words)

chinese_stop_words = set(stopwords.words("chinese"))  # 获取中文停用词列表
print(chinese_stop_words)

sentence = "<p>Hello, World! Here's a <a href='https://example.com'>link</a>.</p>"
clean_text = remove_noise(sentence)
print(clean_text)

tokens_normalized = [token.lower() for token in clean_text]
print(tokens_normalized)

filtered_tokens = [word for word in tokens_normalized if not word in stop_words]
print(filtered_tokens)
