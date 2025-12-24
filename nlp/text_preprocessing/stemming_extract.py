import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# 确保已下载NLTK的tokenizers和corpora
nltk.download('punkt')

# 初始化词干提取器
stemmer = PorterStemmer()
# 示例文本
text = "The leaves on the trees are falling quickly in the autumn season."
# 分词
tokens = word_tokenize(text)
# 词干提取
stemmed_tokens = [stemmer.stem(token) for token in tokens]
print("原始文本:")
print(tokens)
print("\n词干提取后:")
print(stemmed_tokens)
