from flask_restful import Resource
from models.category import CategoryModel


class CategoryList(Resource):
    def get(self):
        categories = CategoryModel.query.all()
        return {"categories": [category.json() for category in categories]}
