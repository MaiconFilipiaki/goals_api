from flask import Flask

from goals.ext import configuration
from goals.ext import database
from goals.ext import migration

from goals.blueprints.api import v1

app = Flask(__name__)
configuration.init_app(app)
database.init_app(app)
migration.init_app(app)

v1.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)