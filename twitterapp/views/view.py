from flask import render_template, request
from twitterapp.services import twitterstream
from twitterapp import app
from twitterapp.models import model


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    if request.method == "POST":
        # get url that the user has entered
        try:
            keyword = request.form['keyword']
            #r = requests.get(keyword)
            #print(r.text)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
        if keyword:
            tsm = twitterstream.TwitterDataStreamer()
            tsm.stream(keyword)
    tweets = model.User.query.all()
    return render_template('index.html', errors=errors, results=tweets)
