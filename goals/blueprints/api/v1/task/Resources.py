from flask import request, jsonify, make_response
from flask_restful import Resource

from goals.ext.database import db
from goals.security.auth import jwt_required

from goals.models.models import Goal, Task
from goals.models.Schemas import task_share_schema, task_share_schemas


class TaskResources(Resource):

    @jwt_required
    def put(self, current_user, id_goals):
        id = request.args.get('id')
        done = request.json.get('done')
        if done is None:
            return make_response(
                jsonify({
                    "error": "You need to fill all field"
                }), 400
            )
        result = Task.query.filter_by(id=id).first()
        if result is None:
            return make_response(
                jsonify({
                    "error": "task not found"
                }), 404
            )
        result.done = done
        db.session.commit()
        result = task_share_schema.dump(
            Goal.query.filter_by(id=id).first()
        )
        return jsonify(result)
