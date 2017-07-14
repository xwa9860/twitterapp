'''
get data and train a model to classify tweets
between nuclear bomb and nuclear energy
'''
from twitterapp.services.topic import TopicModel
topic_model = TopicModel(False, False)
topic_model.test_performance()
topic_model.saveto('twitterapp/services/topic_model')

from twitterapp.services.sentiment import SentModel
model = SentModel()
model.test_performance()
model.saveto('twitterapp/services/sent_model')
