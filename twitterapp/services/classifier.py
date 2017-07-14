'''
build a voter classifier that combines multiple classifiers
'''
import nltk
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from nltk.classify import ClassifierI
from statistics import mode


class VoteClassifier(ClassifierI):
    def __init__(self, classifiers, training_features):
        self._classifiers = classifiers
        for c in self._classifiers:
            c.train(training_features)

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

    def show_performance(self, testset):
        for c in self._classifiers:
            print("Classifier %s accuracy percent:" % c.__class__,
                  (nltk.classify.accuracy(c, testset))*100)
        print("voted_classifier accuracy percent:",
              (nltk.classify.accuracy(self, testset))*100)

    def saveto(self, saveto='classifier'):
        ''' save classifier to file
        '''
        save_classifier = open(saveto, "wb")
        pickle.dump(self, save_classifier)
        save_classifier.close()


class TweetClassifier(VoteClassifier):
    def __init__(self, train_set):
        MNB = SklearnClassifier(MultinomialNB())
        BNB = SklearnClassifier(BernoulliNB())
        LR = SklearnClassifier(LogisticRegression())
        SGD = SklearnClassifier(SGDClassifier())
        LinSVC = SklearnClassifier(LinearSVC())

        VoteClassifier.__init__(self,
                                [LinSVC,
                                 SGD,
                                 MNB,
                                 BNB,
                                 LR],
                                train_set)


class SavedClassifier(object):
    def __init__(self, path):
        with open(path, 'rb') as f:
            self.classifier = pickle.load(f)
