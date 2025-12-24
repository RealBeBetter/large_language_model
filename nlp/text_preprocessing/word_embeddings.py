from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize

# 定义训练语料
sentences = [
    "The cat sat on the mat.",
    "Dogs and cats are enemies.",
    "The dog chased the cat."
]
# 使用NLTK进行分词
tokenized_sentences = [word_tokenize(sentence.lower()) for sentence in sentences]
print(tokenized_sentences)
# 训练Word2Vec模型
model = Word2Vec(sentences=tokenized_sentences, vector_size=100, window=5, min_count=1, workers=4)
# 获取单词“cat”的向量
cat_vector = model.wv['cat']
print("cat的向量表示:\n", cat_vector)
# 找到与“cat”最相似的单词
similar_words = model.wv.most_similar('cat', topn=5)
print("和cat相似的单词是:", similar_words)
