import random
from flask import Response, jsonify
from application import app, db
import requests
from application.models import UserTest, AnsweredQuestion, Question, Test
from sqlalchemy import func


@app.route('/user/matchtestpage/<id>', methods=['GET'])
def random_question(id):
    print('this is the user_id')
    app.logger.info(id)
    user_test = UserTest.query.filter_by(id=id).first()
    #for question in user_test:
    #if answer == question.answer:

    # check the answer
    # - make sure you get the question id from the form
    # - get the data from the form
    # - compare the answer to the questions given

    # get a random question
    unanswered_questions = []
    for question in user_test.answered_questions:
        unanswered_questions.append(question)
    random.shuffle(unanswered_questions)
    answerlist= []
    aidlist = []
    for data in unanswered_questions:
          answerlist.append(data.answer)
          aidlist.append(data.id)
    return jsonify({"a_id":aidlist, "answer":answerlist})

