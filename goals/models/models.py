from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin

from goals.ext.database import db


class User(db.Model, SerializerMixin):
    """ this user reference model """

    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(84), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    goals = db.relationship(
        'Goal',
        cascade="all,delete",
        backref='goal',
        lazy='dynamic'
    )

    def __init__(self, username, email, password, goals):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.goals = goals

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User : {self.username} >'


class Goal(db.Model):
    __tablename__ = 'goal'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.String(150), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    talkies = db.relationship(
        'Task',
        backref='goal',
        cascade="all,delete",
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<Goal: {self.name}>'


class Task(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    value = db.Column(db.String(20), nullable=False)
    done = db.Column(db.Boolean, default=False)
    goal_id = db.Column(
        db.Integer,
        db.ForeignKey('goal.id')
    )
