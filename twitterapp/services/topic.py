'''
train a classifier to distinguish tweets about nuclear bomb
from those about nuclear power
'''
import nltk
import pickle
from twitterapp.services.StatModel import StatModel
from twitterapp.services.preproc import labeled_text_2_featuresets
from twitterapp.models.model import Tweet
import pandas as pd
from twitterapp.services import word_frequency as wf


class TopicModel(StatModel):
    def __init__(self,
                 feature_words_path=None,
                 feature_data_path=None,
                 classifier=None):

        if feature_words_path is not None:
            wordsdf = pd.read_hdf(feature_words_path)
            words = wordsdf['word']
        else:
            print('getting and saving frequent words')
            words = wf.count_words_frequency(5000)
            print(words)
            words.to_hdf('twitterapp/services/frequent_words.hdf',
                         'main', format='fixed')

        if feature_data_path is not None:
            with open(feature_data_path, 'rb') as f:
                features = pickle.load(f)
        else:
            raw_data = self.get_labeled()
            features = labeled_text_2_featuresets(raw_data, words)

        StatModel.__init__(self,
                           words, features,
                           default_classifier=None)

    def get_labeled(self):
        '''
        build a labeled data set by gathering tweets with the specific words
        in it
         c as civil, m as military
        '''
        pnb = 0
        bnb = 0
        dataset = []
        for t in Tweet.query.all():
            tokens = nltk.word_tokenize(t.tweet)
            text = nltk.Text(tokens)
            if any(word.lower() in ['trump', 'weapon', 'war', 'bomb']
                    for word in text):
                dataset.append((text, 'm'))
                bnb += 1
            if any(word.lower() in ['energy', 'electricity']
                   for word in text):
                dataset.append((text, 'c'))
                pnb += 1
        print('power nb %d, bomb nb %d' % (pnb, bnb))
        return dataset


class defaultTopicModel(StatModel):
    def __init__(self):
        path = 'twitterapp/services/topic_model_'
        classifier = pickle.load(open("%sclassifier.pkl" % path, "rb"))
        with open(''.join([path, 'words.pkl']), "rb") as f:
            words = pickle.load(f)
        features = None
        StatModel.__init__(self, words, features, classifier)
