from datetime import datetime
from db import db
from models.question import QuestionModel


class AnswerModel(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(255))
    number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    question = db.relationship(
        'QuestionModel',
        backref=db.backref('answers', cascade='all, delete-orphan',
                           lazy='dynamic')
    )

    def __init__(self, answer, number, question_id):
        self.answer = answer
        self.number = number
        self.add_question(question_id)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def add_question(self, question_id):
        question = QuestionModel.query.filter_by(id=question_id).first()
        self.question = question
