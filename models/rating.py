from db import db


class RatingModel(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    rate = db.Column(db.Integer)
    
    author_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    author = db.relationship(
        'StudentModel',
        backref=db.backref('ratings', cascade='all, delete-orphan',
                           lazy='dynamic')
    )
