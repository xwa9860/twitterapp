from twitterapp import twitter_db
from twitterapp.models.model import Twitteruser, Word, Tweet, Hashtag
from twitterapp.services.sentiment import defaultSentModel
from twitterapp.services.topic import defaultTopicModel
import json
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy import desc


def add_status_to_db(status, db=twitter_db):
    status = status._json

    # add user to database
    uid = status['user']['id']
    u = Twitteruser.query.filter_by(uid=str(uid)).first()
    if not u:
        print('add user to database %s' % twitter_db)
        u = Twitteruser(screen_name=status['user']['screen_name'],
                        uid=uid,
                        follower_count=status['user']["followers_count"])
        db.session.add(u)
        db.session.commit()
    else:
        print('user exists')

    # add tweet and its words to database

    try:
        tid = status['id']
        t = Tweet.query.filter_by(tid=str(tid)).first()
        if not t:
            sent_model = defaultSentModel()
            sent_pred = sent_model.predict(status['text'])
            topic_model = defaultTopicModel()
            topic_pred = topic_model.predict(status['text'])

            print('add tweet to database %s' % twitter_db)
            tw = Tweet(tweet=status['text'],
                       tid=status['id'],
                       user_id=u.id,
                       coordinates=status['coordinates'],
                       created_at=status['created_at'],
                       retweet_count=status['retweet_count'],
                       truncated=status['truncated'],
                       sentiment=sent_pred[0],
                       topic=topic_pred[0],
                       data=json.dumps(status))
            words = tw.tweet.split()
            for w in words:
                try:
                    w_obj = Word.query.filter(Word.word == w).one()
                except MultipleResultsFound:
                    pass
                except NoResultFound:
                    w_obj = Word(word=w)
                    db.session.add(w_obj)
                    db.session.commit()
                    tw.words.append(w_obj)
            db.session.add(tw)
            db.session.commit()
            return tw.tid
        else:
            print('tweet exists')
    except OperationalError:
        print('operational error, database rolling back')
        db.session.rollback()


def get_status_from_db(n):
    tweets = Tweet.query.order_by(desc(Tweet.id)).limit(n).all()
    return tweets
