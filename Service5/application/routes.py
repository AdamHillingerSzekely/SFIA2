from flask import Response, jsonify
from application import app
import requests


@app.route('/user/matchtestpage/<id>', methods=['GET'])
def random_question(id):
    question=requests.get('http://service3:5000/user/matchtestpage/' + id).json()
    answer=requests.get('http://service4:5000/user/matchtestpage/' + id).json()
    return jsonify({"idandquestion":question, "idandanswer":answer})
