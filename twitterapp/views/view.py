from flask import render_template
from flask import request
from flask import jsonify
from sqlalchemy import desc
from twitterapp.services import twitterstream
from twitterapp.services import word_frequency
from twitterapp import app
from twitterapp.models import model
from twitterapp import q
from rq.job import Job
from worker import conn
import time
import json

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.charts import Bar


def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

@app.route('/', methods=['GET', 'POST'])
def index():
    #words = word_frequency.count_words_frequency(20)
    #print(words)
    words = {
    'sample': ['1st', '2nd', '1st', '2nd', '1st', '2nd'],
    'interpreter': ['python', 'python', 'pypy', 'pypy', 'jython', 'jython'],
    'timing': [-2, 5, 12, 40, 22, 30]
        }
    bars = Bar(words, values='timing', label='interpreter', stack='sample', agg='mean',
          title="Python Interpreter Sampling", legend='top_right', width=400)

    #bars = Bar(words, values='count', label='word', legend=False)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(bars)
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        color='#000000'
    )
    return encode_utf8(html)


@app.route('/start', methods=['POST'])
def get_tweets():
    # get 'keyword' from user
    data = json.loads(request.data.decode())
    keyword = data["keyword"]
    print('got keyword from the user %s' % keyword)
    # start job
    job = q.enqueue_call(func=fetch_and_record_tweets,
                         args=([keyword],),
                         result_ttl=5000,
                         timeout=10000)
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




@app.route("/bokeh")
def polynomial():
    """ Very simple embedding of a polynomial chart
    """

    # Grab the inputs arguments from the URL
    #args = request.args

    # Get all the form arguments in the url with defaults
    #color = getitem(args, 'color', 'Black')
    #_from = int(getitem(args, '_from', 0))
    #to = int(getitem(args, 'to', 10))

    #'Black': '#000000',
    # Create a polynomial line graph with those arguments
    x = list(range(0, 10 + 1))
    fig = figure(title="Polynomial")
    fig.line(x, [i ** 2 for i in x], color='#000000', line_width=2)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig)
    html = render_template(
        'embed.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        color='#000000',
        _from=_from,
        to=to
    )
    return encode_utf8(html)
