from config import db, bcrypt
from marshmallow import Schema, fields
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String,
        nullable=False,
        unique=True
    )

    _password_hash = db.Column(db.String)

    # relations
    tasks = db.relationship(
        'Task',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    # password protection
    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash,
            password.encode('utf-8')
        )
    
    # validation
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Username must be present.')

        return username
    
class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()