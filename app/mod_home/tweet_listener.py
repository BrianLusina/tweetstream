from tweepy import Stream, StreamListener


class TweetListener(StreamListener):
    """
    Listener for tweets used for streaming tweets for topics from an observer object
    """

    def __init__(self, observer):
        super().__init__()
        self.observer = observer

    def on_data(self, raw_data):
        self.observer.on_next(raw_data)
        return True

    def on_exception(self, exception):
        super().on_exception(exception)
        self.observer.on_error(exception)

    def on_error(self, status_code):
        self.observer.on_error(status_code)
