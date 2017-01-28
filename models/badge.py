from datetime import datetime
from db import db
from models.user import UserModel
from models.course import CourseModel

users_badges = db.Table('users_badges',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('badge_id', db.Integer, db.ForeignKey('badges.id'))
)


class BadgeModel(db.Model):
    __tablename__ = 'badges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    picture = db.Column(db.String(255))

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship('CourseModel',
        backref=db.backref('badge', uselist=False))

    students = db.relationship('UserModel', secondary=users_badges,
        backref=db.backref('badges', lazy='dynamic'))

    def __init__(self, name, course_id, student_id, picture=None):
        self.name = name
        self.add_course(course_id)
        self.add_student(student_id)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.picture = picture

    def add_course(self, course_id):
        course = CourseModel.query.filter_by(id=course_id).first()
        self.course = course

    def add_student(self, student_id):
        student = UserModel.query.filter_by(id=student_id).first()
        self.students.append(student)
