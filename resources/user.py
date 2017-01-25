from flask_restful import Resource
from models.user import UserModel


class UserList(Resource):
    def get(self):
        users = UserModel.query.all()
        return {"users": [user.json() for user in users]}
