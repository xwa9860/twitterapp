from twitterapp import twitter_db
from twitterapp.models.model import Twitteruser, Word, Tweet, Hashtag
import json
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound


def add_status_to_db(status, db=twitter_db):
    status = status._json

    # add user to database
    uid = status['user']['id']
    u = Twitteruser.query.filter_by(uid=str(uid)).first()
    if not u:
        print('add user to database %s' % twitter_db)
        u = Twitteruser(screen_name=status['user']['screen_name'],
                 uid=uid)
        db.session.add(u)
        db.session.commit()
    else:
        print('user exists')

    # add tweet to database
    tw = Tweet(tweet=status['text'], tid=status['id'], user_id=u.id,
               created_at=status['created_at'], data=json.dumps(status))

    try:
        print('add tweet to database %s' % twitter_db)
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
    except OperationalError:
        print('operational error, database rolling back')
        db.session.rollback()


def get_status_from_db(status_id, db=twitter_db):
    pass
