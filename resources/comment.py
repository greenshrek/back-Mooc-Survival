from flask_restful import Resource
from models.comment import CommentModel


class CommentList(Resource):
    def get(self):
        comments = CommentModel.query.all()
        return {"comments": [comment.json() for comment in comments]}
