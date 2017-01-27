from datetime import datetime
from db import db


class QuestionModel(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255))
    number = db.Column(db.Integer)
    good_answer = db.Column(db.Integer)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    quiz = db.relationship(
        'QuizModel',
        backref=db.backref('questions', cascade='all, delete-orphan',
                           lazy='dynamic')
    )

    def __init__(self, question, number, good_answer):
        self.question = question
        self.number = number
        self.good_answer = good_answer
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
