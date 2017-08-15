import os

basedir = os.path.abspath(os.path.dirname(__file__))
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """
    Global configuration from which other configs inherit
    :cvar THREADS_PER_PAGE: Application threads. A common general assumption is
    using 2 per available processor cores - to handle
    incoming requests using one and performing background
    operations using the other.
    :cvar CSRF_SESSION_KEY Use a secure, unique and absolutely secret key for signing the data.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tweetstream'
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT") or 'tweet_stream_rx'
    ROOT_DIR = APP_ROOT
    WTF_CSRF_ENABLED = True
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = os.environ.get("CSRF_SESSION_KEY")
    THREADS_PER_PAGE = 2

    # credentials for external service accounts
    TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
    TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    Development configuration
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


class TestingConfig(Config):
    """
    Testing configurations
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    """
    Production configuration
    """
    ADMINS = [os.environ.get("ADMIN_EMAIL")]


config = {
    'develop': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
