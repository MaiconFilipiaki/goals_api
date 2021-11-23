from flask import Blueprint
from flask_restful import Api

from .login.Resources import LoginResource
from .user.Resources import UserResource
from .goal.Resources import GoalResource
from .task.Resources import TaskResources

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

api.add_resource(UserResource, '/user', endpoint='user')
api.add_resource(LoginResource, '/auth', endpoint='auth')
api.add_resource(GoalResource, '/goal', endpoint='goal')
api.add_resource(TaskResources, '/goal/<id_goals>/task')

def init_app(app):
    app.register_blueprint(api_bp)
