from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from application import app, db, bcrypt
from application.models import Posts, Users, Test, Question, AnsweredQuestion, UserTest
from application.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm, TakeTest, AnswerVerification, QuestionGenerator, TestComment, TakeMatchTest
import random
import requests



@app.route('/')
@app.route('/home')
def home():
        postData = Posts.query.all()
        return render_template('home.html', title='Home', posts=postData)

@app.route('/about')
def about():
        return render_template('about.html', title='About')


@app.route('/question_set', methods=['GET', 'POST'])
def question_set():
    form = TakeTest()
    return render_template('questionbankupload.html', title='Question Set', form=form)


@app.route('/match_question_set', methods=['GET', 'POST'])
def match_question_set():
    form= TakeMatchTest()
    return render_template('matchquestionbankupload.html', title='Match Test Set', form=form)


@app.route('/user/matchtestpage/<id>')
def matchtestpage(id):
       data=requests.get('http://service5:5000/user/matchtestpage/' + id).json()
       print(data)
       idplusquestion = data["idandquestion"]
       idplusanswer = data["idandanswer"]
       question = idplusquestion["question"]
       question_id = idplusquestion["q_id"]
       answer = idplusanswer["answer"]
       answer_id = idplusanswer["a_id"]
       return render_template('matchtestpage.html', title='The Matchtest', data=data, question=question, answer=answer, test_id=id, question_id=question_id)
    #else:
        #return redirect(url_for('analysismatch', test_id=id)

@app.route('/user/test/create')
def user_test_create():
    test = Test.query.filter_by(id=1).first()
    user_questions = []
    #print('creating user questions')
    for question in test.questions:
        user_questions.append(AnsweredQuestion(question=question.question, answer=question.answer, attempts = 0))
    #print('creating user test')
    user_test = UserTest(answered_questions=user_questions)
    db.session.add(user_test)
    db.session.commit()
    db.session.refresh(user_test)
    return redirect(url_for('testpage', id=user_test.id))

@app.route('/user/matchtest/create')
def user_match_test_create():
    test = Test.query.filter_by(id=1).first()
    user_questions = []
    #print('creating user questions')
    for question in test.questions:
        user_questions.append(AnsweredQuestion(question=question.question, answer=question.answer, attempts = 0))
    #print('creating user test')
    user_test = UserTest(answered_questions=user_questions)
    db.session.add(user_test)
    db.session.commit()
    db.session.refresh(user_test)
    return redirect(url_for('matchtestpage', id=user_test.id))



@app.route('/user/testpage/<id>')
def testpage(id):
    form = QuestionGenerator()
    data=requests.get('http://service2:5000/user/testpage/'  + id).json()
    if data["id"] != 0:
         question_id = data["id"]
         question = data["question"]
         return render_template('testpage.html', title='The Test', question=question, form=form, test_id=id, question_id=question_id)
    # render_template('user-test.html', question=question)
    else:
        print('all questions answered, going to the results')
        return redirect(url_for('analysis', test_id=id))

@app.route('/test/<test_id>/question/<question_id>', methods=['POST'])
def user_question(test_id, question_id):
    answered_question = AnsweredQuestion.query.filter_by(id=question_id).first()
    app.logger.info(answered_question)
    form = QuestionGenerator()
    user_answer = form.question.data
    print("Actual answer: " + answered_question.answer + "\nUser answer: " + user_answer)
    if answered_question.answer == user_answer:
        answered_question.completed = True
        print('answer is correct !')
    else:
        print('answer is incorrect !')
        answered_question.attempts = answered_question.attempts + 1
    db.session.add(answered_question)
    db.session.commit()
    return redirect(url_for('testpage', id=test_id))



@app.route('/test/<test_id>/analysis', methods=['GET', 'POST'])
def analysis(test_id):
        results=AnsweredQuestion.query.filter_by(user_test_id=test_id)
        form = TestComment()
        if form.validate_on_submit():
                Comment = Posts(
                comment = form.comment.data,
                title = form.title.data,
                content = form.content.data,
                author=current_user)
                db.session.add(Comment)
                db.session.commit()
                return redirect(url_for('home'))
        return render_template('analysis.html', results=results, form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
        if current_user.is_authenticated:
                return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
                user=Users.query.filter_by(email=form.email.data).first()
                if user and bcrypt.check_password_hash(user.password, form.password.data):
                        login_user(user, remember=form.remember.data)
                        next_page = request.args.get('next')
                        if next_page:
                                return redirect(next_page)
                        else:
                                return redirect(url_for('home'))
        return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=[ 'GET', 'POST'])
def register():
        if current_user.is_authenticated:
                return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
                hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

                user = Users(
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email = form.email.data,
                        password = hash_pw
                )

                db.session.add(user)
                db.session.commit()

                return redirect(url_for('post'))
        return render_template('register.html', title='Register', form=form)

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
        form = PostForm()
        if form.validate_on_submit():
                postData = Posts(
                        title = form.title.data,
                        content = form.content.data,
                        author=current_user
                )

                db.session.add(postData)
                db.session.commit()

                return redirect(url_for('home'))
        else:
                print(form.errors)

        return render_template('post.html', title='Post', form=form)





@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
        form = UpdateAccountForm()
        if form.validate_on_submit():
                current_user.first_name = form.first_name.data
                current_user.last_name = form.last_name.data
                current_user.email = form.email.data
                db.session.commit()
                return redirect(url_for('account'))
        elif request.method == 'GET':
                form.first_name.data = current_user.first_name
                form.last_name.data = current_user.last_name
                form.email.data = current_user.email
        return render_template('account.html', title='Account', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
        user = current_user.id

        account = Users.query.filter_by(id=user).first()
        posts= Posts.query.filter_by(user_id=user).all()
        logout_user()
        for post in posts:
                        db.session.delete(post)
        db.session.delete(account)
        db.session.commit()
        return redirect(url_for('register'))



@app.route("/post/delete/<id>", methods=["GET", "POST"])
@login_required
def delete_post(id):
        deleter = Posts.query.filter_by(id=id).first()
        db.session.delete(deleter)
        db.session.commit()
        return redirect(url_for('home'))

