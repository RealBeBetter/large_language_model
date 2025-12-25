from gensim.models import Word2Vec

# 加载模型
model = Word2Vec.load("word2vec.model")
print("模型加载完成")

# 类比
result = model.wv.evaluate_word_pairs("valid.tsv")
print(result)
