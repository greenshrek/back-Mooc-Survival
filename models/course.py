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
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    comments = db.relationship('CommentModel', backref='courses', lazy='dynamic')

    def __init__(self, title, content, owner_id, category_id):
        self.title = title
        self.content = content
        self.date = datetime.now()
        self.owner = UserModel.find_by_id(owner_id)
        self.category = CategoryModel.find_by_id(category_id)

    def json(self):
        return {
            "title": self.title,
            "content": self.content,
            "created_at": self.date.strftime("%d/%m/%y - %H:%M:%S"),
            "created_by": self.owner.json(),
            "category": self.category.json(),
            "coments": [comment.json() for comment in self.comments.all()]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, course_id):
        return cls.query.filter_by(id=course_id).first()
