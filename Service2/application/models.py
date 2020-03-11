from application import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class AnsweredQuestion(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   user_test_id = db.Column(db.Integer, db.ForeignKey('user_test.id'))
   question = db.Column(db.String(1000), nullable=False)
   answer = db.Column(db.String(1000), nullable=False)
   attempts = db.Column(db.Integer)
   completed = db.Column(db.Boolean, unique=False, default=False)

class UserTest(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   answered_questions = db.relationship('AnsweredQuestion', backref='answered_question', lazy=False)


class Question(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
   question = db.Column(db.String(1000), nullable=False)
   answer = db.Column(db.String(1000), nullable=False)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questions = db.relationship('Question', backref='test_question', lazy=False)

