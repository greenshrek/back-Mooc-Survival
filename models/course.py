from datetime import datetime
from db import db
from models.user import UserModel
from models.category import CategoryModel

class CourseModel(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    content = db.Column(db.Text())
    date = db.Column(db.DateTime())

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('UserModel',
                             backref=db.backref('courses',
                                                cascade='all, delete-orphan',
                                                lazy='dynamic'))

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('CategoryModel',
                               backref=db.backref('courses',
                                                  cascade='all, delete-orphan',
                                                  lazy='dynamic'))

    def __init__(self, title, content, author_id, category_id):
        self.title = title
        self.content = content
        self.date = datetime.utcnow()
        self.author = UserModel.find_by_id(author_id)
        self.category = CategoryModel.find_by_id(category_id)

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
