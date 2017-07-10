'''
train a classifier to distinguish tweets about nuclear bomb
from those about nuclear power
'''
from twitterapp.models.model import Tweet
import nltk
import pickle
import time
import pandas as pd


def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print ('%r %2.2f sec' %
               (method.__name__, te-ts))
        return result

    return timed


@timeit
def data_set():
    raw = power_or_bomb()
    featuresets = [(feature_array(text), category) for (text, category) in raw]
    print('built featuresets')
    with open('twitterapp/services/data', 'wb') as fp:
        pickle.dump(featuresets, fp)
    return featuresets
    print(featuresets)

@timeit
def power_or_bomb():
    '''
    build a labeled training set by gathering tweets with the specific words in it
     c as civil, m as military
    '''

    pnb = 0
    bnb = 0
    train = []
    for t in Tweet.query.all():
        nltk.data.path.append('./nltk_data/')  # set the path
        tokens = nltk.word_tokenize(t.tweet)
        text = nltk.Text(tokens)
        if any(word in ['weapon', 'war', 'bomb'] for word in text):
            train.append((text, 'm'))
            bnb += 1
        if any(word in ['energy', 'plant','power'] for word in text):
            train.append((text, 'c'))
            pnb += 1
    print('power nb %d, bomb nb %d' % (pnb, bnb))
    return train
    print(power_or_bomb)


def feature_array(text):
    '''
     build an array of booleans for each feature word
     1 if it is in the text, 0 if not
    feature word is the most often used words in the text of
    the training dataset
    '''
    wordsdf = pd.read_hdf('twitterapp/services/frequent_words.hdf')
    words = wordsdf['word']
    text = set(text)
    features = {}
    for w in words:
        features[w] = (w in text)
    return features


@timeit
def model(data):
    tot_len = len(data)
    print(tot_len)
    training_set = data[:int(tot_len/5*4)]
    testing_set = data[int(tot_len/5*4):]
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print('done')
    save_classifier = open("naivebayes.pickle", "wb")
    pickle.dump(classifier, save_classifier)
    save_classifier.close()
    print("Classifier accuracy percent:",
          (nltk.classify.accuracy(classifier, testing_set))*100)
    classifier.show_most_informative_features(15)
    print(model)


def predict(tweet):
    '''
    tweet: Tweet object
    '''
    tokens = nltk.word_tokenize(tweet)
    text = nltk.Text(tokens)
    features = feature_array(text)
    classifier_f = open("naivebayes.pickle", "rb")
    classifier = pickle.load(classifier_f)
    classifier_f.close()
    c = classifier.classify(features)
    print(tweet.text)
    print(c)
    return c


def label_dataset():

    for t in Tweet.query.all():
        predict(t)
