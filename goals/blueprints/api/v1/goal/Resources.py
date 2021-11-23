from flask import jsonify, request, make_response
from flask_restful import Resource

from goals.security.auth import jwt_required

from goals.ext.database import db
from goals.models.models import Goal, Task
from goals.models.Schemas import goal_share_schema, goal_share_schemas


class GoalResource(Resource):

    @jwt_required
    def post(self, current_user):
        description = request.json.get('description')
        price = request.json.get('price')
        months = request.json.get('months')
        if description is None:
            return jsonify({
                "error": "Required description"
            }), 422
        if price is None:
            return jsonify({
                "error": "Required price"
            }), 422
        if months is None:
            return jsonify({
                "error": "Required months"
            }), 422
        priceWithDot = str(price).replace(',', '.')
        valueMonth = float(priceWithDot) / float(months)
        print(valueMonth)
        goal = Goal(
            description=description,
            price=price,
            talkies=[],
            user_id=current_user.id
        )
        db.session.add(goal)
        db.session.flush()
        idGoal = goal.id
        db.session.commit()
        rangesLimit = (range(int(months)))
        talkies = []
        for i in rangesLimit:
            talk = Task(
                value = str(valueMonth).replace('.', ','),
                done = False,
                goal_id = idGoal
            )
            talkies.append(talk)
        db.session.add_all(talkies)
        db.session.commit()
        result = goal_share_schema.dump(
            Goal.query.filter_by(id=idGoal).first()
        )
        return make_response(
            jsonify(result),
            201
        )

    @jwt_required
    def delete(self, current_user):
        id = request.args.get('id')
        if id is None:
            return make_response(
                jsonify({'error': 'You need to inform an id'}),
                400
            )
        result = Goal.query.filter_by(id=id).first()
        if bool(result) is False:
            return make_response(
                jsonify({'error': 'goal not found'}),
                404
            )
        db.session.delete(result)
        db.session.commit()
        return jsonify({"msg": "goal deleted with success"})

    @jwt_required
    def get(self, current_user):
        id = request.args.get('id')
        if id is None:
            result = goal_share_schemas.dump(
                Goal.query.filter_by(user_id=current_user.id)
            )
            return jsonify(result)
        result = goal_share_schema.dump(
            Goal.query.filter_by(id=id).first()
        )
        if bool(result) is False:
            return make_response(
                jsonify({'error': 'prompt delivery not found'}),
                404
            )
        return jsonify(result)
