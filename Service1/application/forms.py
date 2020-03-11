from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users
from application import app
from flask_login import current_user

class PostForm(FlaskForm):
    title = StringField('Title',
        validators = [
            DataRequired(),
            Length(min=2, max=100)
        ]
    )
    content = StringField('Content',
        validators = [
            DataRequired(),
            Length(min=2, max=1000)
        ]
    )
    submit = SubmitField('Post!')


class RegistrationForm(FlaskForm):
	first_name = StringField('First Name',
		validators = [
			DataRequired(),
            		Length(min=2, max=30)
		]
	)
	last_name = StringField('Last Name',
		validators = [
			DataRequired(),
			Length(min=2, max=30)
		]
	)
	email = StringField('Email',
		validators = [
			DataRequired(),
			Email()
		]
	)
	password = PasswordField('Password',
		validators = [
			DataRequired(),
		]
	)
	confirm_password = PasswordField('Confirm Password', 
		validators = [
			DataRequired(),
			EqualTo('password')
		]
	)
	submit = SubmitField('Sign Up')

	def validate_email(self, email):
		user = Users.query.filter_by(email=email.data).first()

		if user:
			raise ValidationError('Email already in use')





class TakeTest(FlaskForm):
	submit = SubmitField('Take Test')

class TakeMatchTest(FlaskForm):
	submit = SubmitField('Match Test Set')

class LoginForm(FlaskForm):
	email = StringField('Email',
		validators=[
			DataRequired(),
			Email()
		]
	)

	password = PasswordField('Password',
		validators=[
			DataRequired()
		]
	)

	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class TestComment(FlaskForm):
	comment = StringField('Comment',
		validators=[
			DataRequired(),
			Length(min=4, max=100)
		]
	)
	title = StringField('Title',
		validators = [
			DataRequired(),
			Length(min=2, max=100)
		]
	)
	content = StringField('Content',
		validators = [
			DataRequired(),
			Length(min=2, max=1000)
		]
	)
	submit = SubmitField('Submit Comment')

class UpdateAccountForm(FlaskForm):
	first_name = StringField('First Name',
		validators=[
			DataRequired(),
			Length(min=4, max=30)
		])
	last_name = StringField('Last Name',
		validators=[
			DataRequired(),
			Length(min=4, max=30)
		])
	email = StringField('Email',
		validators=[
			DataRequired(),
			Email()
		])
	submit = SubmitField('Update')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = Users.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email already in use')



class QuestionGenerator(FlaskForm):
	question = StringField('Question',
		validators=[
			DataRequired(),
			Length(min=4, max=100)
		])
	submit = SubmitField('Submit Answer')



class AnswerVerification(FlaskForm):
	answer = StringField('Answer',
		validators=[
			DataRequired(),
			Length(min=4, max=100)
		])
	submit = SubmitField('Submit')
