'''
build a statistics model for the data
'''
import nltk
import random
from twitterapp.services.classifier import TweetClassifier
from twitterapp.models import db_crud
from twitterapp.services.preproc import text2features
import pickle


class StatModel(object):

    def __init__(self, words,
                 features,
                 default_classifier=None):

        if default_classifier:
            self.classifier = default_classifier
        else:
            tot_len = len(features)
            random.shuffle(features)
            self.training_features = features[:int(tot_len/2)]
            self.testing_features = features[int(tot_len/2):]
            self.classifier = TweetClassifier(self.training_features)
        self.words = words
        self.features = features

    def saveto(self, saveto):
        with open(''.join([saveto, 'classfier.pkl']), "wb") as f:
            pickle.dump(self.classifier, f)
        with open(''.join([saveto, 'words.pkl']), "wb") as f:
            pickle.dump(self.words, f)
        with open(''.join([saveto, 'features.pkl']), "wb") as f:
            pickle.dump(self.training_features, f)

    def test_performance(self):
        self.classifier.show_performance(self.testing_features)
        for tweet in db_crud.get_status_from_db(10):
            nltk.data.path.append('./nltk_data/')  # set the path
            tokens = nltk.word_tokenize(tweet.tweet)
            text = nltk.Text(tokens)
            text = set(text)
            features = text2features(text, self.words)
            print(self.classifier.classify(features))
            print(self.classifier.confidence(features))

    def predict(self, text):
        nltk.data.path.append('./nltk_data/')  # set the path
        tokens = nltk.word_tokenize(text)
        text = nltk.Text(tokens)
        text = set(text)
        features = text2features(text, self.words)
        return (self.classifier.classify(features),
                self.classifier.confidence(features))
