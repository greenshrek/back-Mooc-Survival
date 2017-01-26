from db import db


class BadgeModel(db.Model):
    __tablename__ = 'badges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    picture = db.Column(db.String(255))

    author_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    author = db.relationship(
        'StudentModel',
        backref=db.backref('badges', cascade='all, delete-orphan',
                           lazy='dynamic')
    )
