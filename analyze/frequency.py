import nltk
import pandas

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')


def most_frequent_stopwords(content, max_amount):
    words = filter(lambda w: w not in stopwords and w != "", content.split(" "))
    return pandas.Series(words).value_counts().head(max_amount)

