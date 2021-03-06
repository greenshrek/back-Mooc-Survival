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

    def __init__(self, title, content, author_id, category_id, picture):
        self.title = title
        self.content = content
        self.add_author(author_id)
        self.add_category(category_id)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.picture = picture

    def add_author(self, author_id):
        author = UserModel.query.filter_by(id=author_id).first()
        self.author = author

    def add_category(self, category_id):
        category = CategoryModel.query.filter_by(id=category_id).first()
        self.category = category

    def register_student(self, student_id):
        student = UserModel.query.filter_by(id=student_id).first()
        self.students.append(student)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        self.title = kwargs['title']
        self.content = kwargs['content']
        self.picture = kwargs['picture']
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%dT%H:%M:%S'),
            "author": {
                "id": self.author.id,
                "username": self.author.username
            },
            "category": {
                "id": self.category.id,
                "name": self.category.name
            },
            "comments": [comment.json() for comment in self.comments],
            "students": [student.json() for student in self.students],
            "chapters": [chapter.json() for chapter in self.chapters],
            "quizzes": [quiz.json() for quiz in self.quizzes],
            "steps": [step.json() for step in self.steps]
        }

    def json_light(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%dT%H:%M:%S'),
            "author": {
                "id": self.author.id,
                "username": self.author.username
            },
            "category": {
                "id": self.category.id,
                "name": self.category.name
            }
        }


    @classmethod
    def find_by_id(cls, course_id):
        return cls.query.filter_by(id=course_id).first()
