from datetime import datetime
from db import db
from models.user import UserModel
from models.course import CourseModel


class StepModel(db.Model):
    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True)
    current_step = db.Column(db.Integer)
    final_step = db.Column(db.Integer)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    student = db.relationship('UserModel',
        backref=db.backref('steps', cascade='all, delete-orphan',
                           lazy='dynamic')
    )
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship('CourseModel',
        backref=db.backref('steps', cascade='all, delete-orphan',
                           lazy='dynamic')
    )

    def __init__(self, current_step, final_step, student_id, course_id):
        self.current_step = current_step
        self.final_step = final_step
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.add_student(student_id)
        self.add_course(course_id)

    def add_student(self, student_id):
        student = UserModel.find_by_id(student_id)
        self.student = student

    def add_course(self, course_id):
        course = CourseModel.find_by_id(course_id)
        self.course = course

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        self.current_step = kwargs['current_step']
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "current_step": self.current_step,
            "final_step": self.final_step,
            "student": {
                "id": self.student.id,
                "username": self.student.username
            },
            "course": {
                "id": self.course.id,
                "title": self.course.title
            }
        }

    @classmethod
    def find_by_id(cls, step_id):
        return cls.query.filter_by(id=step_id).first()
