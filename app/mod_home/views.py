from . import home
from flask import current_app
from tweepy import StreamListener, Stream, OAuthHandler
from rx import Observable
from .tweet_listener import TweetListener
import json


@home.route("")
@home.route("home")
@home.route("index")
def index():
    topics = ["Britain", "France", "Kenya"]
    tweets_for(topics) \
        .map(lambda d: json.loads(d)) \
        .subscribe(on_next=lambda s: print(s), on_error=lambda e: print(e))


def tweets_for(topics):
    """
    Returns an observable from TweetListener
    :param topics: topics to get streams for
    """

    def observe_tweets(observer):
        """
        :param observer: Observable object which will emit streams
        :return:
        """
        twitter_consumer_key = current_app.config.get("TWITTER_CONSUMER_KEY")
        twitter_secret = current_app.config.get("TWITTER_CONSUMER_SECRET")
        listener = TweetListener(observer)
        auth = OAuthHandler(twitter_consumer_key, twitter_secret)
        stream = Stream(auth, listener)
        stream.filter(topics)

    return Observable.create(observe_tweets).share()
