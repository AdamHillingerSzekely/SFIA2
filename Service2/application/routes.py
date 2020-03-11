import random
from flask import Response, jsonify
from application import app, db
import requests
from application.models import UserTest, AnsweredQuestion, Question, Test
from sqlalchemy import func


@app.route('/user/testpage/<id>', methods=['GET'])
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
        if not question.completed:
            unanswered_questions.append(question)
    print(unanswered_questions)
    if unanswered_questions:
        quest = random.choice(unanswered_questions)
        q = quest.question
        qid= quest.id
        app.logger.info(quest.id)
        return jsonify({"id":qid, "question":q})
    else:
        return jsonify({"id":0, "question":'No questions'})
