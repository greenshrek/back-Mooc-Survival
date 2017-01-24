from db import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    courses = db.relationship('CourseModel', backref='categories', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            "id": self.id,
            "category_name": self.name,
            "courses": [course.json() for course in self.courses.all()]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, category_id):
        return cls.query.filter_by(id=category_id).first()
