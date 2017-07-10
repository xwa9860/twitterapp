from twitterapp.models.model import Twitteruser, Word, Tweet, Hashtag
from collections import Counter
from twitterapp.services.stops import stops
import re
import pandas as pd
import nltk
from nltk.stem import PorterStemmer

def count_words_frequency(n, raw_data=Tweet.query.all()):
    ps = PorterStemmer()

    #count word_frequency in the last ten tweets
    word_count = Counter()

    for t in raw_data:
        nltk.data.path.append('./nltk_data/')  # set the path
        tokens = nltk.word_tokenize(t.tweet)
        text = nltk.Text(tokens)

        # remove punctuation, count raw words
        nonPunct = re.compile('.*[A-Za-z].*')
        for w in text:
            if nonPunct.match(w) and w.lower() not in stops:
                word_count[w.lower()] += 1
    res = word_count.most_common(n)
    res = pd.DataFrame(res, columns=['word', 'count'])
    return res

def count_named_entity(n, raw_data):

    #count word_frequency in the last ten tweets
    word_count = Counter()

    for t in raw_data:
        nltk.data.path.append('./nltk_data/')  # set the path
        tokens = nltk.word_tokenize(t.tweet)
        text = nltk.Text(tokens)

        # remove punctuation, count raw words
        nonPunct = re.compile('.*[A-Za-z].*')
        for w in text:
            if nonPunct.match(w) and w not in stops:
                word_count[w] += 1
    res = word_count.most_common(n)
    res = pd.DataFrame(res, columns=['word', 'count'])
    return res


def save_frequent_words():
    raw_data = Tweet.query.all()
    f = count_words_frequency(3000, raw_data)
    f.to_hdf('twitterapp/services/frequent_words.hdf', 'main', format='fixed')
