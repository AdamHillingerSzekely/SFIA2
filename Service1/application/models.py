from application import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 

    def __repr__(self):
        return ''.join([
            'User ID: ', self.user_id, '\r\n',
            'Title: ', self.title, '\r\n', self.content
            ])

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    posts = db.relationship('Posts', backref='author', lazy=True)
    def __repr__(self):
        return ''.join([
		'UserID: ', str(self.id), '\r\n',
		'Email: ', self.email, '\r\n',
		'Name: ', self.first_name, ' ', self.last_name
	])

class Question(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
   question = db.Column(db.String(1000), nullable=False)
   answer = db.Column(db.String(1000), nullable=False)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questions = db.relationship('Question', backref='test_question', lazy=False)


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





class MatchTest(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   qandarelation = db.relationship('QuestionsDatabase', backref='answered_question', lazy=False)

class QuestionsDatabase(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   user_test_id = db.Column(db.Integer, db.ForeignKey('match_test.id'))
   question = db.Column(db.String(1000), nullable=False)
   answer = db.Column(db.String(1000), nullable=False)


