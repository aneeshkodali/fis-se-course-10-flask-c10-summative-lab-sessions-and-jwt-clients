from config import db
from marshmallow import Schema, fields
from sqlalchemy.orm import validates


class Task(db.Model):
    __tablename__ = 'tasks'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(
        db.String,
        nullable=False
    )
    description = db.Column(db.String)
    priority = db.Column(
        db.String,
        default='medium'
    )
    status = db.Column(
        db.String,
        default='not started'
    )
    due_date = db.Column(db.Date)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    # relations
    user = db.relationship(
        'User',
        back_populates='tasks'
    )

    # validation
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Title must be present.')

        return title

    @validates('priority')
    def validate_priority(self, key, priority):
        if priority not in ['low', 'medium', 'high']:
            raise ValueError('Priority must be low, medium, or high.')

        return priority

    @validates('status')
    def validate_status(self, key, status):
        if status not in ['not started', 'in progress', 'complete']:
            raise ValueError(
                'Status must be not started, in progress, or complete.'
            )

        return status


class TaskSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    priority = fields.Str()
    status = fields.Str()
    due_date = fields.Date()
    user_id = fields.Int()

    user = fields.Nested(
        'UserSchema',
        exclude=('tasks',)
    )