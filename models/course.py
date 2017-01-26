from datetime import datetime
from db import db
from models.user import InstructorModel
from models.category import CategoryModel


students_courses = db.Table('students_courses',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')))


class CourseModel(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    content = db.Column(db.Text())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    picture = db.Column(db.String(255))

    author_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    author = db.relationship(
        'InstructorModel',
        backref=db.backref('courses', cascade='all, delete-orphan',
                           lazy='dynamic')
    )
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship(
        'CategoryModel',
        backref=db.backref('courses', cascade='all, delete-orphan',
                           lazy='dynamic')
    )
    students = db.relationship('StudentModel', secondary=students_courses,
        backref=db.backref('enrolled_courses', lazy='dynamic'))

    def __init__(self, title, content, author_id, category_id):
        self.title = title
        self.content = content
        self.date = datetime.utcnow()
        self.author = InstructorModel.find_by_id(author_id)
        self.category = CategoryModel.find_by_id(category_id)

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.date.strftime("%d/%m/%y - %H:%M:%S"),
            # "author": {
            #     "id": self.author.id,
            #     "username": self.author.username
            # },
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
