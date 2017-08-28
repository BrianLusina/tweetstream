import json

from flask import current_app, request, render_template
from rx import Observable
from tweepy import Stream, OAuthHandler
from .forms import TopicsForm
from . import home
from .tweet_listener import TweetListener
from pprint import pprint


@home.route("", methods=["POST", "GET"])
def index():
    topics_form = TopicsForm(request.form)
    tweet_stream = None
    context = {
        "topics_form": topics_form,
        "topic_tweets": []
    }
    if request.method == "POST":
        if topics_form.validate_on_submit():
            topics = topics_form.topic_name.data

            tweets_for(topics).map(lambda d: json.loads(d)) \
                .subscribe(on_next=lambda s: context["topic_tweets"].append(format_tweet(s)),
                           on_error=lambda e: print("Error found => ", e))

    topics = ["Kenya"]
    return tweets_for(topics).map(lambda d: json.loads(d)) \
        .subscribe(on_next=lambda s: pprint(s),
                   on_error=lambda e: print("Error found => ", e))

    return render_template("home.topics.html", **context)


def format_tweet(tweet):
    """
    Formats a tweet to understandable data for display
    :param tweet: tweet from tweet stream
    :return: a nicely formated tweet
    """
    pass


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
