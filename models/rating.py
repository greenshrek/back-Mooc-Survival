from datetime import datetime
from db import db
from models.course import CourseModel
from models.user import UserModel


class RatingModel(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    rate = db.Column(db.Integer)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship(
        'UserModel',
        backref=db.backref('ratings', cascade='all, delete-orphan',
                           lazy='dynamic')
    )
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship(
        'CourseModel',
        backref=db.backref('ratings', cascade='all, delete-orphan',
                           lazy='dynamic')
    )

    def __init__(self, rate, course_id, author_id):
        self.rate = rate
        self.add_course(course_id)
        self.add_author(author_id)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def add_course(self, course_id):
        course = CourseModel.query.filter_by(id=course_id).first()
        self.course = course

    def add_author(self, author_id):
        author = UserModel.query.filter_by(id=author_id).first()
        self.author = author
