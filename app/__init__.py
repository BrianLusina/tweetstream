import os

import jinja2
from flask import Flask

from config import config


class TweetStreamApp(Flask):
    """
    Custom flask application for the entire application
    """

    def __init__(self):
        """
        jinja_loader object (a FileSystemLoader pointing to the global templates folder)
        is being replaced with a ChoiceLoader object that will first search the normal
        FileSystemLoader and then check a PrefixLoader that we create
        """
        Flask.__init__(self, __name__, template_folder="templates", static_folder="static")
        self.jinja_loader = jinja2.ChoiceLoader([
            self.jinja_loader,
            jinja2.PrefixLoader({}, delimiter=".")
        ])

    def create_global_jinja_loader(self):
        return self.jinja_loader

    def register_blueprint(self, blueprint, **options):
        Flask.register_blueprint(self, blueprint, **options)
        self.jinja_loader.loaders[1].mapping[blueprint.name] = blueprint.jinja_loader


def create_app(config_name):
    """
    Defines a new application WSGI. Creates the flask application object that will be used
    to define and create the whole application
    :param config_name: the configuration to use when creating a new application
    :return: the newly created and configured WSGI Flask object
    :rtype: Flask
    """
    app = TweetStreamApp()

    # configurations
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_blueprints(app)
    set_logger(app, config_name)

    # increases performance of loading application templates
    app.jinja_env.cache = {}

    return app


def set_logger(app, config_name):
    """
    Sets logging of error messages in case they occur in the application. This will send an email to
    any of the administrators, or all of the administrators.
    This should work when the application is in production
    Will also record any errors to a log file
    RotatingFileHandler is used to limit the number of logs to 1MB and limit the backup to 10 files
    logging.formatter will enable us to format the log messages and get the line number that brought up the issue as
    well as the stack trace.
    :param app: current Flask app
    :param config_name: the configuration to use this, normally in Production
    """
    import logging
    from logging.handlers import SMTPHandler, RotatingFileHandler
    MAIL_SERVER = app.config.get("MAIL_SERVER")

    if config_name == "production":
        if not app.debug and MAIL_SERVER != "":
            credentials = None

            MAIL_USERNAME = app.config.get("MAIL_USERNAME")
            MAIL_PASSWORD = app.config.get("MAIL_PASSWORD")

            if MAIL_USERNAME or MAIL_PASSWORD:
                credentials = (MAIL_USERNAME, MAIL_PASSWORD)

            mail_handler = SMTPHandler(mailhost=(MAIL_SERVER, app.config.get("MAIL_HOST")),
                                       fromaddr="no-reply@" + MAIL_SERVER,
                                       toaddrs=app.config.get("ADMINS"),
                                       subject="Hadithi app failure",
                                       credentials=credentials)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not app.debug and os.environ.get("HEROKU") is None:
            # log file will be saved in the tmp directory
            file_handler = RotatingFileHandler(filename="tmp/hadithi.log", mode="a", maxBytes=1 * 1024 * 1024,
                                               backupCount=10)
            file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%('
                                                        'lineno)d]'))
            app.logger.setLevel(logging.INFO)
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.info("Hadithi Blog")


def register_blueprints(app_):
    """
    Registers tall blueprints in the app
    :param app: The current flask application
    """
    from app.mod_home import home

    app_.register_blueprint(home)
