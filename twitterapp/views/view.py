from flask import render_template, request
from flask import jsonify
from sqlalchemy import desc
from twitterapp.services import twitterstream
from twitterapp import app
from twitterapp.models import model
from twitterapp import q
from rq.job import Job
from worker import conn
import time
import json


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def get_tweets():
    # get 'keyword' from user
    data = json.loads(request.data.decode())
    keyword = data["keyword"]
    print(keyword)
    # start job
    job = q.enqueue_call(func=fetch_and_record_tweets,
                         args=([keyword],),
                         result_ttl=5000)
    print(job.get_id())
    return job.get_id()


def fetch_and_record_tweets(keywords):
    '''
    To be processed correctly in job.result, this function should always return string
    '''
    tsm = twitterstream.TwitterDataStreamer()
    tsm.stream(keywords)

    # create a dictionary to hold the results

    return 'job done'


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        print('job finished')
        cols = ['tid', 'tweet']
        new_tweets = model.Tweet.query.order_by(desc(model.Tweet.id)).limit(2).all()
        res = [{col: getattr(d, col) for col in cols} for d in new_tweets]
        return jsonify(result=res), 200
    else:
        return "Nay!", 202