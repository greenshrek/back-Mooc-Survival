from flask_restful import Resource, reqparse
from models.category import CategoryModel

parser = reqparse.RequestParser()
parser.add_argument('name',
                    required=True,
                    help="A name must be provided.")
parser.add_argument('fr_label')
parser.add_argument('en_label')
parser.add_argument('picture')

class Category(Resource):

    def get(self, category_id):
        category = CategoryModel.find_by_id(category_id)

        if category is None:
            return {"message": "Category not found."}, 404

        return category.json(), 201

    def put(self, category_id):
        data = parser.parse_args()

        category = CategoryModel.find_by_id(category_id)

        if category is None:
            new_category = CategoryModel(**data)

            try:
                new_category.save()

                return new_category.json(), 201
            except:
                return {"message": "An error occurred while inserting Category"}, 500

        try:
            category.update(**data)
        except:
            return {"message": "An error occurred while updating Category."}, 500

        return category.json(), 200

    def delete(self, category_id):
        category = CategoryModel.find_by_id(category_id)

        if category is None:
            return {"message": "Category not found."}, 404

        try:
            category.delete()
        except:
            return {"message": "An error occurred while deleting Category."}, 500

        return {"message": "Category deleted."}, 200

class CategoryList(Resource):

    def get(self):
        categories = CategoryModel.query.all()
        return [category.json() for category in categories]

    def post(self):
        data = parser.parse_args()

        if CategoryModel.query.filter_by(name=data['name']).first():
            msg = "A category with name:'{}' already exists.".format(
                data['name'])
            return {"message": msg}, 400

        category = CategoryModel(**data)
        try:
            category.save()
        except:
            return {"message": "An error occurred while inserting Category"}, 500

        return category.json(), 201
