from datetime import datetime
from db import db


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

    def __init__(self, rate):
        self.rate = rate
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
