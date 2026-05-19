from config import (
    db,
    api,
    app,
)
from flask import (
    make_response,
    request,
    session,
)
from flask_restful import Resource
from models import (
    Task,
    TaskSchema,
    User,
    UserSchema,
)
from sqlalchemy.exc import IntegrityError

user_schema = UserSchema()
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

def current_user():
    '''
    Find the logged-in user.
    '''

    user_id = session.get('user_id')

    if user_id:
        return User.query.filter_by(id=user_id).first()

    return None

class Signup(Resource):
    def post(self):
        data = request.get_json() or {}

        if not data.get('username') or not data.get('password'):
            return make_response(
                {'errors': ['Username and password are required.']},
                422
            )

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
        data = request.get_json() or {}

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
    
class TaskIndex(Resource):
    def get(self):
        user = current_user()

        if not user:
            return make_response(
                {'errors': ['Unauthorized']},
                401
            )

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        pagination = Task.query.filter_by(user_id=user.id).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return make_response(
            {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'total_pages': pagination.pages,
                'items': tasks_schema.dump(pagination.items)
            },
            200
        )

    def post(self):
        user = current_user()

        if not user:
            return make_response(
                {'errors': ['Unauthorized']},
                401
            )

        data = request.get_json() or {}

        try:
            task = Task(
                title=data.get('title'),
                description=data.get('description'),
                priority=data.get('priority', 'medium'),
                status=data.get('status', 'not started'),
                due_date=data.get('due_date'),
                user_id=user.id
            )

            db.session.add(task)
            db.session.commit()

            return make_response(task_schema.dump(task), 201)

        except ValueError as e:
            db.session.rollback()

            return make_response(
                {'errors': [str(e)]},
                422
            )

class TaskById(Resource):
    def patch(self, id):
        user = current_user()

        if not user:
            return make_response(
                {'errors': ['Unauthorized']},
                401
            )

        # filter by user
        task = Task.query.filter_by(id=id, user_id=user.id).first()

        if not task:
            return make_response(
                {'errors': ['Task not found']},
                404
            )

        data = request.get_json() or {}

        try:
            for attr in ['title', 'description', 'priority', 'status', 'due_date']:
                if attr in data:
                    setattr(task, attr, data.get(attr))

            db.session.commit()

            return make_response(task_schema.dump(task), 200)

        except ValueError as e:
            db.session.rollback()

            return make_response(
                {'errors': [str(e)]},
                422
            )

    def delete(self, id):
        user = current_user()

        if not user:
            return make_response(
                {'errors': ['Unauthorized']},
                401
            )

        # filter by user
        task = Task.query.filter_by(id=id, user_id=user.id).first()

        if not task:
            return make_response(
                {'errors': ['Task not found']},
                404
            )

        db.session.delete(task)
        db.session.commit()

        return {}, 204

# register 
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(TaskById, '/tasks/<int:id>', endpoint='task_by_id')
api.add_resource(TaskIndex, '/tasks', endpoint='tasks')

if __name__ == '__main__':
    app.run(port=5555, debug=True)