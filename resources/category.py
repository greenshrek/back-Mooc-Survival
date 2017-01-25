from flask_restful import Resource, reqparse
from models.category import CategoryModel


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
            category.save_to_db()
        except:
            return {"message": "An error occured while inserting Category"}, 500

        return category.json(), 201
