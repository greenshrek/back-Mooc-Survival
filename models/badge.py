from datetime import datetime
from db import db

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

    def __init__(self, name, picture=None):
        self.name = name
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.picture = picture
