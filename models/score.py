from datetime import datetime
from db import db
from models.user import UserModel
from models.quiz import QuizModel


class ScoreModel(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    max_score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    student = db.relationship(
        'UserModel',
        backref=db.backref('scores', cascade='all, delete-orphan',
                           lazy='dynamic')
    )
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    quiz = db.relationship(
        'QuizModel',
        backref=db.backref('scores', cascade='all, delete-orphan',
                           lazy='dynamic')
    )

    def __init__(self, score, max_score, student_id, quiz_id):
        self.score = score
        self.max_score = max_score
        self.add_student(student_id)
        self.add_quiz(quiz_id)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def add_student(self, student_id):
        student = UserModel.query.filter_by(id=student_id).first()
        self.student = student

    def add_quiz(self, quiz_id):
        quiz = QuizModel.query.filter_by(id=quiz_id).first()
        self.quiz = quiz

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        self.score = kwargs['score']
        self.max_score = kwargs['max_score']
        self.updated_at = datetime.now()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "score": self.score,
            "max_score": self.max_score,
            "created_at": self.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%dT%H:%M:%S'),
            "quiz": {
                "id": self.quiz.id,
                "title": self.quiz.title
            },
            "student": {
                "id": self.student.id,
                "title": self.student.username
            }
        }

    @classmethod
    def find_by_id(cls, score_id):
        return cls.query.filter_by(id=score_id).first()

    @classmethod
    def find_by_quiz(cls, quiz_id):
        return cls.query.filter_by(quiz_id=quiz_id).all()
