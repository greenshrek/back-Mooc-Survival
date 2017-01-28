from datetime import datetime
from db import db
from models.user import UserModel
from models.category import CategoryModel


enrolled_courses = db.Table('enrolled_courses',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


class CourseModel(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    content = db.Column(db.Text())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    picture = db.Column(db.String(255))

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship(
        'UserModel',
        backref=db.backref('published_courses', cascade='all, delete-orphan',
                           lazy='dynamic')
    )
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship(
        'CategoryModel',
        backref=db.backref('courses', cascade='all, delete-orphan',
                           lazy='dynamic')
    )
    students = db.relationship('UserModel', secondary=enrolled_courses,
        backref=db.backref('enrolled_courses', lazy='dynamic'))

    def __init__(self, title, content, author, category, picture=None):
        self.title = title
        self.content = content
        self.add_author(author)
        self.add_category(category)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.picture = picture

    def add_author(self, author_name):
        author = UserModel.query.filter_by(username=author_name).first()
        self.author = author

    def add_category(self, category_name):
        category = CategoryModel.query.filter_by(name=category_name).first()
        self.category = category

    def register_student(self, student_name):
        student = UserModel.query.filter_by(username=student_name).first()
        self.students.append(student)

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.date.strftime("%d/%m/%y - %H:%M:%S"),
            "author": {
                "id": self.author.id,
                "username": self.author.username
            },
            "category": {
                "id": self.category.id,
                "name": self.category.name
            },
            "comments": [comment.json() for comment in self.comments.all()]
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        if kwargs['title']:
            self.title = kwargs['title']
        if kwargs['content']:
            self.content = kwargs['content']
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, course_id):
        return cls.query.filter_by(id=course_id).first()
