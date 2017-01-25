from flask_restful import Resource, reqparse
from models.category import CategoryModel


class Category(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name')

    def get(self, category_id):
        category = CategoryModel.find_by_id(category_id)

        if category is None:
            return {"message": "Category not found."}, 404

        return category.json(), 201

    def put(self, category_id):
        data = self.parser.parse_args()

        category = CategoryModel.find_by_id(category_id)

        if category is None:
            return {"message": "Category not found."}, 404

        try:
            category.update(**data)
        except:
            return {"message": "An error occured while updating Category."}, 500

        return category.json(), 200

    def delete(self, category_id):
        category = CategoryModel.find_by_id(category_id)

        if category is None:
            return {"message": "Category not found."}, 404

        try:
            category.delete()
        except:
            return {"message": "An error occured while deleting Category."}, 500

        return {"message": "Category deleted."}, 200

class CategoryList(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True)

    def get(self):
        categories = CategoryModel.query.all()
        return {"categories": [category.json() for category in categories]}

    def post(self):
        data = self.parser.parse_args()

        if CategoryModel.query.filter_by(name=data['name']).first():
            msg = "A category with name:'{}' already exists.".format(
                data['name'])
            return {"message": msg}, 400

        category = CategoryModel(**data)
        try:
            category.save()
        except:
            return {"message": "An error occured while inserting Category"}, 500

        return category.json(), 201
