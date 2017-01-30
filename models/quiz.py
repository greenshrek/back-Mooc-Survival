from datetime import datetime
from db import db
from models.course import CourseModel


class QuizModel(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship(
        'CourseModel',
        backref=db.backref('quizzes', cascade='all, delete-orphan',
                           lazy='dynamic')
    )

    def __init__(self, title, number, course_id):
        self.title = title
        self.number = number
        self.add_course(course_id)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def add_course(self, course_id):
        course = CourseModel.query.filter_by(id=course_id).first()
        self.course = course

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        self.title = kwargs['title']
        self.number = kwargs['number']
        self.updated_at = datetime.now()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "number": self.number,
            "created_at": self.created_at.strftime("%d/%m/%y"),
            "updated_at": self.updated_at.strftime("%d/%m/%y"),
            "course": {
                "id": self.course.id,
                "title": self.course.title
            },
            "questions": [question.json() for question in self.questions]
        }

    @classmethod
    def find_by_id(cls, quiz_id):
        return cls.query.filter_by(id=quiz_id).first()

    @classmethod
    def find_by_course(cls, course_id):
        return cls.query.filter_by(course_id=course_id).all()
