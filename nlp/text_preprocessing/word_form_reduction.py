from nltk.stem import WordNetLemmatizer
import nltk
from nltk.tokenize import word_tokenize

# 确保已下载wordnet和averaged_perceptron_tagger
nltk.download('wordnet')
text = "The leaves on the trees are falling quickly in the autumn season."
# 分词
tokens = word_tokenize(text)
# 初始化词形还原器
lemmatizer = WordNetLemmatizer()
# 词形还原（默认为名词）
lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
print("原始文本:")
print(tokens)
print("\n词形还原:")
print(lemmatized_tokens)
