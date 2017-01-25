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
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    comments = db.relationship('CommentModel', backref='courses', lazy='dynamic')

    def __init__(self, title, content, author_id, category_id):
        self.title = title
        self.content = content
        self.date = datetime.now()
        self.author_id = author_id
        self.category_id = category_id

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.date.strftime("%d/%m/%y - %H:%M:%S"),
            "created_by": self.get_author(),
            "category": self.get_category(),
            "comments": [comment.json() for comment in self.comments.all()]
        }

    def get_author(self):
        author = UserModel.query.filter_by(id=self.author_id).first()
        return {"id": author.id, "name": author.username}

    def get_category(self):
        category = CategoryModel.query.filter_by(id=self.category_id).first()
        return {"id": category.id, "name": category.name}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, course_id):
        return cls.query.filter_by(id=course_id).first()
