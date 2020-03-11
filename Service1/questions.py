import csv
from application import db
from application.models import Question, Test
import pandas as pd



csv_path = './RandDtest.csv'



data = pd.read_csv(csv_path)
data.columns=['question', 'answer']

questions = []


for index, row in data.iterrows():
        question = Question(question=row[0], answer=row[1])
        questions.append(question)

test = Test(questions=questions)
db.session.add(test)
db.session.commit()

#for index, row in data.iterrows():
        #answer =Answers(answer=row[1])
        #db.session.add(answer)
# db.session.commit()


