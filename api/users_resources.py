from __future__ import unicode_literals
from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User
from api.parsers import parserForUser


def abort_if_questions_not_found(user_id):
    session = db_session.create_session()
    if user_id.isdigit():
        users = session.query(User).get(user_id)
        if not users:
            abort(404, message=f"User {user_id} not found")
    else:
        abort(404, message=f"User id is not integer")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_questions_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify(
            {
                'user':
                    user.to_dict(only=('id', 'name', 'surname', 'nickname', 'email', 'rating'))
            }
        )


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()

        return jsonify(
            {
                'users':
                    [user.to_dict(only=('id', 'name', 'surname', 'nickname', 'email', 'rating')) for user in users]
            }
        )