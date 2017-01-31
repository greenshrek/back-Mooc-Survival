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

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        self.answer = kwargs['answer']
        self.number = kwargs['number']
        self.updated_at = datetime.now()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "answer": self.answer,
            "number": self.number,
            "created_at": self.created_at.strftime("%d/%m/%y"),
            "updated_at": self.updated_at.strftime("%d/%m/%y"),
            "question": {
                "id": self.question.id,
                "question": self.question.question
            }
        }

    @classmethod
    def find_by_id(cls, answer_id):
        return cls.query.filter_by(id=answer_id).first()

    @classmethod
    def find_by_question(cls, question_id):
        return cls.query.filter_by(question_id=question_id).all()
