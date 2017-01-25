from flask_restful import Resource, reqparse
from models.user import UserModel


class UserList(Resource):

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

    def get(self):
        users = UserModel.query.all()
        return {"users": [user.json() for user in users]}

    def post(self):
        data = self.parser.parse_args()

        if UserModel.query.filter_by(username=data['username']).first():
            msg = "A user with username:'{}' already exists.".format(
                data['username'])
            return {"message": msg}, 400

        user = UserModel(**data)
        try:
            user.save_to_db()
        except:
            return {"message": "An error occured while inserting User."}, 500

        return user.json(), 201
