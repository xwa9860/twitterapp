from flask import render_template
from flask import request
from flask import jsonify
from twitterapp.services import twitterstream
from twitterapp.services import named_entity as ne
from twitterapp.services import word_frequency as wf
from twitterapp.models import db_crud
from twitterapp import app
from twitterapp import q
import json
import random


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def get_tweets():
    # get 'keyword' from user
    data = json.loads(request.data.decode())
    keyword = data["keyword"]
    print('got keyword from the user %s' % keyword)
    # start job
    job = q.enqueue_call(func=fetch_and_record_tweets,
                         args=([keyword],),
                         result_ttl=5000, timeout=5000)
    print(job.get_id())
    return job.get_id()


def fetch_and_record_tweets(keywords):
    '''
    To be processed correctly in job.result,
    this function should always return string
    '''
    tsm = twitterstream.TwitterDataStreamer()
    tsm.stream(keywords)
    return 'job done'


@app.route("/results", methods=['GET'])
def get_results():
    cols = ['tid', 'tweet']
    new_tweets = db_crud.get_status_from_db(1)
    res = [{col: getattr(d, col) for col in cols} for d in new_tweets]
    return jsonify(result=res), 200


@app.route("/neg_words", methods=['GET'])
def get_words():
    words = ne.nltk_main('neg')
    print(words)
    res = [{'text': word[0],
            'size': random.randint(10, 100)} for word in words]
    return jsonify(result=res), 200


@app.route("/pos_words", methods=['GET'])
def get_pos_words():
    words = ne.nltk_main('pos')
    print(words)
    res = [{'text': word[0],
            'size': random.randint(10, 100)} for word in words]
    return jsonify(result=res), 200
