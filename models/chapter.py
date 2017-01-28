from datetime import datetime
from db import db


chapters_courses = db.Table('chapters_courses',
    db.Column('chapter_id', db.Integer, db.ForeignKey('chapters.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
)

class ChapterModel(db.Model):
    __tablename__ = 'chapters'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    courses = db.relationship('CourseModel', secondary=chapters_courses,
        backref=db.backref('chapters', lazy='dynamic'))

    def __init__(self, title, content, number):
        self.title = title
        self.content = content
        self.number = number
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
