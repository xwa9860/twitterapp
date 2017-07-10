
from twitterapp.services import topic
import pickle

with open('twitterapp/services/data', 'rb') as f:
    data = pickle.load(f)
topic.model(data)
