from config import app, api, db
from flask import make_response, request, session
from flask_restful import Resource
from models import User, UserSchema, Task
from sqlalchemy.exc import IntegrityError

user_schema = UserSchema()

class Signup(Resource):
    def post(self):
        data = request.get_json()

        if data.get('password') != data.get('password_confirmation'):
            return make_response(
                {'errors': ['Password confirmation does not match.']},
                422
            )

        try:
            user = User(username=data.get('username'))
            user.password_hash = data.get('password')

            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id

            return make_response(user_schema.dump(user), 201)

        except (ValueError, IntegrityError) as e:
            db.session.rollback()

            return make_response(
                {'errors': [str(e)]},
                422
            )


class Login(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return make_response(user_schema.dump(user), 200)

        return make_response(
            {'errors': ['Invalid username or password.']},
            401
        )


class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')

        if user_id:
            user = User.query.filter_by(id=user_id).first()

            if user:
                return make_response(user_schema.dump(user), 200)

        return make_response({}, 401)


class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session.pop('user_id')
            return {}, 204

        return make_response(
            {'errors': ['Unauthorized']},
            401
        )

# register 
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)