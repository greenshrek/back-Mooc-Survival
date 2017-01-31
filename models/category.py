from datetime import datetime
from db import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    fr_label = db.Column(db.String(255))
    en_label = db.Column(db.String(255))
    picture = db.Column(db.String(255))

    def __init__(self, name, fr_label, en_label, picture):
        self.name = name
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.fr_label = fr_label
        self.en_label = en_label
        self.picture = picture

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        self.name = kwargs['name']
        self.fr_label = kwargs['fr_label']
        self.en_label = kwargs['en_label']
        self.picture = kwargs['picture']
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "category_name": self.name,
            "created_at": self.created_at.strftime("%d/%m/%y"),
            "updated_at": self.updated_at.strftime("%d/%m/%y"),
            "french_label": self.fr_label,
            "english_label": self.en_label,
            "picture_url": self.picture,
            "courses": [course.json() for course in self.courses]
        }

    @classmethod
    def find_by_id(cls, category_id):
        return cls.query.filter_by(id=category_id).first()
