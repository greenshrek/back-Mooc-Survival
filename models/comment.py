from datetime import datetime
from db import db
from models.user import UserModel
from models.course import CourseModel


class CommentModel(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    date = db.Column(db.DateTime())
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content, course_id, author_id):
        self.content = content
        self.date = datetime.now()
        self.course = CourseModel.find_by_id(course_id)
        self.author = UserModel.find_by_id(author_id)

    def json(self):
        return {
            "content": self.content,
            "created_at": self.date.strftime("%d/%m/%y - %H:%M:%S"),
            "course": self.course.json(),
            "author": self.author.json()
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, comment_id):
        return cls.query.filter_by(id=comment_id).first()
