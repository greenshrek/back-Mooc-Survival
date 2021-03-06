from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.user import UserModel

parser = reqparse.RequestParser()
parser.add_argument('username',
                    required=True,
                    help="A username must be provided.")
parser.add_argument('email',
                    required=True,
                    help="A user email must be provided.")
parser.add_argument('password',
                    required=True,
                    help="A user password must be provided.")
parser.add_argument('role',
                    required=True,
                    help="A user role must be provided.")
parser.add_argument('picture')
parser.add_argument('firstname')
parser.add_argument('lastname')


class UserId(Resource):
    @jwt_required()
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)

        if user is None:
            return {"message": "User not found."}, 404

        return user.json(), 200


class User(Resource):
    method_decorators = [jwt_required()]

    def get(self, username):
        user = UserModel.find_by_username(username)

        if user is None:
            return {"message": "User not found."}, 404

        return user.json(), 201

    def put(self, username):
        data = parser.parse_args()

        user = UserModel.find_by_username(username)

        if user is None:
            new_user = UserModel(**data)
            try:
                new_user.save()

                return new_user.json(), 201
            except:
                return {"message": "An error occurred while inserting User."}, 500

        try:
            user.update(**data)
        except:
            return {"message": "An error occurred while updating User."}, 500

        return user.json(), 200

    def delete(self, username):
        user = UserModel.find_by_username(username)

        if user is None:
            return {"message": "User not found."}, 404

        try:
            user.delete()
        except:
            return {"message": "An error occurred while deleting User."}, 500

        return {"message": "User deleted."}, 200


class UserRegister(Resource):

    def post(self):
        data = parser.parse_args()

        if UserModel.query.filter_by(username=data['username']).first():
            msg = "A user with username:'{}' already exists.".format(
                data['username'])
            return {"message": msg}, 400

        user = UserModel(**data)
        try:
            user.save()
        except:
            return {"message": "An error occurred while inserting User."}, 500

        return user.json(), 201
