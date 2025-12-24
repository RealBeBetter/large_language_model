from sklearn.feature_extraction.text import CountVectorizer

corpus = [
    'Text analysis is fun',
    'Text analysis with Python and backend services with Go',
    'Data Science is fun',
    'Python is great for text analysis'
]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
print(vectorizer.get_feature_names_out())
print(X.toarray())
