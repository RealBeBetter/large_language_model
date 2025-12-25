# 加载模型
from gensim.models import Word2Vec

model = Word2Vec.load("word2vec.model")
print("模型加载完成")

# 使用模型
# 获取一个词的向量
print(model.wv['科技'])

# 找到最相似的词
similar_words = model.wv.most_similar('科技', topn=5)
print(similar_words)
