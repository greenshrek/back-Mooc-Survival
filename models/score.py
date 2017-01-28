from datetime import datetime
from db import db


class ScoreModel(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    max_score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    students = db.relationship(
        'UserModel',
        backref=db.backref('scores', cascade='all, delete-orphan',
                           lazy='dynamic')
    )
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    quizzes = db.relationship(
        'QuizModel',
        backref=db.backref('scores', cascade='all, delete-orphan',
                           lazy='dynamic')
    )

    def __init__(self, score, max_score):
        self.score = score
        self.max_score = max_score
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
