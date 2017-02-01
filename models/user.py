from datetime import datetime
from db import db
from werkzeug.security import generate_password_hash, check_password_hash


users_roles = db.Table('users_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class RoleModel(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    users = db.relationship('UserModel', secondary=users_roles,
        backref=db.backref('roles', lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            "id": self.id,
            "name": self.name
        }


class UserModel(db.Model):
    __tablename__ = 'users'

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
                 role, firstname, lastname, picture):
        self.username = username
        self.set_password(password)
        self.email = email
        self.add_role(role)
        self.firstname = firstname
        self.lastname = lastname
        self.picture = picture
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def add_role(self, role_name):
        role = RoleModel.query.filter_by(name=role_name).first()
        self.roles.append(role)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        self.username = kwargs['username']
        self.email = kwargs['email']
        self.role = kwargs['role']
        self.firstname = kwargs['firstname']
        self.lastname = kwargs['lastname']
        self.picture = kwargs['picture']
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "picture_url": self.picture,
            "roles": [role.json() for role in self.roles],
            "badges": [badge.json() for badge in self.badges]
        }

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
