'''
compute sentiment of each tweet as a score
'''
import nltk
import random
from twitterapp.services.StatModel import StatModel
from twitterapp.services.preproc import labeled_text_2_featuresets
import pickle


class SentModel(StatModel):
    def __init__(self):
        short_pos = open("twitterapp/services/positive.txt",
                         "r", encoding='latin-1').read()
        short_neg = open("twitterapp/services/negative.txt",
                         "r", encoding='latin-1').read()

        documents = []

        for r in short_pos.split('\n'):
            documents.append((r, "pos"))

        for r in short_neg.split('\n'):
            documents.append((r, "neg"))

        all_words = []
        short_pos_words = nltk.word_tokenize(short_pos)
        short_neg_words = nltk.word_tokenize(short_neg)
        for w in short_pos_words:
            all_words.append(w.lower())

        for w in short_neg_words:
            all_words.append(w.lower())
        all_words = nltk.FreqDist(all_words)
        word_features = list(all_words.keys())[:5000]

        featuresets = labeled_text_2_featuresets(documents, word_features)

        random.shuffle(featuresets)
        StatModel.__init__(self, word_features,
                           featuresets)


class defaultSentModel(StatModel):
    def __init__(self):
        path = 'twitterapp/services/sent_model_'
        classifier = pickle.load(open("%sclassifier.pkl" % path, "rb"))
        with open(''.join([path, 'words.pkl']), "rb") as f:
            words = pickle.load(f)
        features = None
        StatModel.__init__(self, words, features, classifier)
