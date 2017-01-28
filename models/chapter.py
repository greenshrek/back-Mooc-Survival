from datetime import datetime
from db import db
from models.course import CourseModel


class ChapterModel(db.Model):
    __tablename__ = 'chapters'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship(
        'CourseModel',
        backref=db.backref('chapters', cascade='all, delete-orphan',
                           lazy='dynamic')
    )

    def __init__(self, title, content, number, course_id):
        self.title = title
        self.content = content
        self.number = number
        self.add_course(course_id)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def add_course(self, course_id):
        course = CourseModel.query.filter_by(id=course_id).first()
        self.course = course
