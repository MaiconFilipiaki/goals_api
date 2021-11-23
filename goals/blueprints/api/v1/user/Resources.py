from flask import jsonify, request, make_response
from flask_restful import Resource

from goals.ext.database import db
from goals.models.models import User
from goals.models.Schemas import user_share_schema
from goals.security.auth import jwt_required


class UserResource(Resource):

    def post(self):
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        if username is None or email is None or password is None:
            return make_response(
                jsonify({"error": "All fields need filled"}),
                400
            )
        
        verifyUserExist = User.query.filter_by(email=email).first()
        if verifyUserExist is not None:
            return make_response(
                jsonify({"error": "E-mail already registered"}),
                400
            )

        user = User(
            username=username,
            email=email,
            password=password,
            goals=[]
        )

        db.session.add(user)
        db.session.commit()
        result = user_share_schema.dump(
            User.query.filter_by(email=email).first()
        )
        return jsonify(result)

    @jwt_required
    def get(self, current_user):
        userJson = user_share_schema.dump(
            current_user
        )
        return jsonify({"user": userJson});
