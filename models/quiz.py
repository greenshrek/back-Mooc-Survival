from datetime import datetime
from db import db


quizzes_courses = db.Table('quizzes_courses',
    db.Column('quiz_id', db.Integer, db.ForeignKey('quizzes.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
)

class QuizModel(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    courses = db.relationship('CourseModel', secondary=quizzes_courses,
        backref=db.backref('quizzes', lazy='dynamic'))

    def __init__(self, title, number):
        self.title = title
        self.number = number
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
