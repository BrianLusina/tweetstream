import json

from flask import current_app
from rx import Observable
from tweepy import Stream, OAuthHandler

from . import home
from .tweet_listener import TweetListener


@home.route("")
@home.route("home")
@home.route("index")
def index():
    topics = ["Britain", "France", "Kenya"]
    return tweets_for(topics) \
        .map(lambda d: json.loads(d)) \
        .subscribe(on_next=lambda s: print(s),
                   on_error=lambda e: print("Error found => ", e))


def tweets_for(topics):
    """
    Returns an observable from TweetListener
    :param topics: topics to get streams for
    :return: Observable object
    """

    def observe_tweets(observer):
        """
        :param observer: Observable object which will emit streams
        """
        twitter_consumer_key = current_app.config.get("TWITTER_CONSUMER_KEY")
        twitter_secret = current_app.config.get("TWITTER_CONSUMER_SECRET")
        twitter_access_token = current_app.config.get("TWITTER_ACCESS_TOKEN")
        twitter_access_token_secret = current_app.config.get("TWITTER_ACCESS_TOKEN_SECRET")

        listener = TweetListener(observer)
        auth = OAuthHandler(consumer_key=twitter_consumer_key, consumer_secret=twitter_secret)
        auth.set_access_token(key=twitter_access_token, secret=twitter_access_token_secret)

        stream = Stream(auth, listener)
        stream.filter(track=topics)

    return Observable.create(observe_tweets).share()
