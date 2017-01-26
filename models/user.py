from datetime import datetime
from db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, username, password, email,
                 firstname, lastname, picture):
        self.username = username
        self.set_password(password)
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.picture = picture
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        if kwargs['username']:
            self.username = kwargs['username']
        if kwargs['email']:
            self.email = kwargs['email']
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()


class StudentModel(db.Model, User):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    picture = db.Column(db.String(255))

    def __init__(self, username, password, email,
                 firstname=None, lastname=None, picture=None):
        User.__init__(self, username, password, email,
                     firstname, lastname, picture)

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            # "courses": [course.json() for course in self.courses.all()],
            # "comments": [comment.json() for comment in self.comments.all()]
        }

    def add_course(self):
        pass


class InstructorModel(db.Model, User):
    __tablename__ = 'instructors'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    picture = db.Column(db.String(255))

    def __init__(self, username, password, email,
                 firstname=None, lastname=None, picture=None):
        User.__init__(self, username, password, email,
                     firstname, lastname, picture)

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            # "courses": [course.json() for course in self.courses.all()],
            # "comments": [comment.json() for comment in self.comments.all()]
        }

    def add_course(self):
        pass
