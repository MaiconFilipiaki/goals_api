from flask import Flask

from goals.ext import configuration
from goals.ext import database
from goals.ext import migration

from goals.blueprints.api import v1

def create_app():
    app = Flask(__name__)
    configuration.init_app(app)
    database.init_app(app)
    migration.init_app(app)

    v1.init_app(app)
    return app