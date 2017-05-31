from twitterapp import twitter_db
from twitterapp.models.model import User, Word, Tweet, Hashtag
import json


def add_status_to_db(status, db=twitter_db):
    status = status._json
    print(status['user']['id'])
    u = User.query.filter_by(
        uid=str(status['user']['id'])).first()
    if not u:
        u = User(screen_name=status['user']['screen_name'],
                 uid=status['user']['id'])
        db.session.add(u)
        db.session.commit()

    #tw = Tweet(tweet=status['text'], tid=status['id'], user_id=u.id,
    #           created_at=status['created_at'], data=json.dumps(status))

    #try:
    #    words = tw.tweet.split()
    #    for w in words:
    #        try:
    #            w_obj = db.session.query(Word).filter(Word.word == w).one()
    #        except MultipleResultsFound:
    #            pass
    #        except NoResultFound:
    #            w_obj = Word(word=w)
    #            db.session.add(w_obj)
    #            db.session.commit()
    #            tw.words.append(w_obj)
    #    db.session.add(tw)
    #    db.session.commit()
    #except OperationalError:
    #    db.session.rollback()


def get_status_from_db(status_id, db=twitter_db):
    pass
