import os
import xml.etree.ElementTree as ET

import jieba
from gensim.models import Word2Vec

# 预处理XML文件，替换特殊字符，解决无法读取这个 XML 文件的问题
# original_text_data.xml Download From https://www.oschina.net/news/82926/google-open-source-seq2seq
original_path = 'original_text_data.xml'
target_path = 'text_data.xml'
if not os.path.exists(target_path):
    with open(original_path, 'r', encoding='utf-8', ) as f1:
        with open(target_path, 'a+', encoding='utf-8') as f2:
            line = f1.readline()
            while line:
                # print(line.strip())
                f2.write(line.replace('&brvbar;', '¦').replace('￿', ''))
                line = f1.readline()

# 读取XML文件并解析
file_path = target_path
tree = ET.parse(file_path)
root = tree.getroot()

# 获取所有<article>标签的内容
texts = [record.find('article').text for record in root.findall('RECORD')]
print(len(texts))

# 停用词列表，实际应用中需要根据实际情况扩展
stop_words = {"的", "了", "在", "是", "我", "有", "和", "就"}

# 分词和去除停用词
processed_texts = []
for text in texts:
    if text is not None:
        words = jieba.cut(text)
        processed_text = [word for word in words if word not in stop_words]
        processed_texts.append(processed_text)

# 打印预处理后的文本
i = 0
for text in processed_texts:
    i += 1
    print(text)
    if i >= 10:
        print("Too many examples, stop printing...")
        break

print(f"Total processed texts: {len(processed_texts)}")

# 训练 Word2Vec模型：
# vector_size表示词向量的维度，sg=1表示使用 Skip-gram 模型，SG=0表示使用 CBOW 模型
# workers表示使用的线程数，window 表示上下文窗口大小，min_count 表示忽略出现次数小于该值的单词
model = Word2Vec(sentences=processed_texts, vector_size=100, window=5, min_count=1, workers=4, sg=0, negative=1)
# 保存模型
model.save("word2vec.model")
