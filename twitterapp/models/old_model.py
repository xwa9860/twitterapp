from twitterapp import twitter_db
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

Base = twitter_db.Model

hashtag_tweet = Table('hashtag_tweet',
                      Base.metadata,
                      Column('hashtag_id', Integer,
                             ForeignKey('hashtag.id'), nullable=False),
                      Column('tweet_id', Integer,
                             ForeignKey('tweet.id'), nullable=False))

hashtag_user = Table('hashtag_user',
                     Base.metadata,
                     Column('hashtag_id', Integer,
                            ForeignKey('hashtag.id'), nullable=False),
                     Column('user_id', Integer,
                            ForeignKey('twitteruser.id'), nullable=False))

tweet_word = Table('tweet_word',
                   Base.metadata,
                   Column('tweet_id', Integer,
                          ForeignKey('tweet.id'), nullable=False),
                   Column('word_id', Integer,
                          ForeignKey('word.id'), nullable=False))


class Hashtag(Base):
    __tablename__ = 'hashtag'
    id = Column(Integer, primary_key=True)
    hashtag = Column(String(200), nullable=False)
    users = relationship('Twitteruser', backref='hashtags',
                         secondary='hashtag_user')
    tweets = relationship('Tweet', backref='hashtags',
                          secondary='hashtag_tweet')

    def __repr(self):
        return '<Hashtag {}>'.format(self.hashtag)


class Tweet(Base):
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    tweet = Column(String(300), nullable=False)
    tid = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('twitteruser.id'), nullable=False)
    coordinates = Column(String(50), nullable=True)
    user = relationship('Twitteruser', backref='tweets')
    words = relationship('Word', backref='tweets', secondary=tweet_word)
    created_at = Column(String(100), nullable=False)
    data = Column(Text, nullable=False)
    # retweet_count = Column(Integer, nullable=True)
    # sentiment = Column(String(50), nullable=True)
    # topic = Column(String(50), nullable=True)

    def __repr__(self):
        return '<Tweet {}>'.format(self.tid)


class Twitteruser(Base):
    __tablename__ = 'twitteruser'
    id = Column(Integer, primary_key=True)
    screen_name = Column(String(100), nullable=False)
    uid = Column(String(50), nullable=False)
    # follower_count = Column(Integer, nullable=False)

    def __repr__(self):
        return '<Twitteruser {}>'.format(self.uid)


class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    word = Column(String(100), nullable=False)

    def __repr__(self):
        return '<Word {}>'.format(self.id)
