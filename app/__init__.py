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

    # increases performance of loading application templates
    app.jinja_env.cache = {}

    return app


def register_blueprints(app_):
    """
    Registers tall blueprints in the app
    :param app: The current flask application
    """
    from app.mod_home import home

    app_.register_blueprint(home)
