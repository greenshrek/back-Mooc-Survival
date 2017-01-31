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

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        self.rate = kwargs['rate']
        self.updated_at = datetime.now()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "rate": self.rate,
            "created_at": self.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%dT%H:%M:%S'),
            "course": {
                "id": self.course.id,
                "title": self.course.title
            },
            "author" : {
                "id": self.author.id,
                "username": self.author.username
            }
        }

    @classmethod
    def find_by_id(cls, rating_id):
        return cls.query.filter_by(id=rating_id).first()

    @classmethod
    def find_by_course(cls, course_id):
        return cls.query.filter_by(course_id=course_id).all()
