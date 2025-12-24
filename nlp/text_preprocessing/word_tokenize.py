import nltk
from nltk.tokenize import word_tokenize

# Download the necessary NLTK resources
nltk.download('punkt')
nltk.download('punkt_tab')

text = "Natural language processing (NLP) is a field of computer science."
tokens = word_tokenize(text)
print(tokens)
