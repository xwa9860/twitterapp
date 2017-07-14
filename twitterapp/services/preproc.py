'''
turn raw tweet into feature set for classify
'''
import pickle

def text2features(text, feature_words):
    '''
     build an array of booleans for each feature word
     1 if it is in the text, 0 if not
    feature word is the most often used words in the text of
    the training dataset
    '''
    features = {}
    for w in feature_words:
        features[w] = (w in text)
    return features


def labeled_text_2_featuresets(labeled_texts, feature_words, saveto=None):
    featuresets = [(text2features(text, feature_words), category)
                   for (text, category) in labeled_texts]

    if saveto:
        with open(saveto, 'wb') as fp:
            pickle.dump(featuresets, fp)

    return featuresets
