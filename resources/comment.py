from flask_restful import Resource, reqparse
from models.comment import CommentModel


class Comment(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('title')
    parser.add_argument('content')

    def get(self, comment_id):
        comment = CommentModel.find_by_id(comment_id)

        if comment is None:
            return {"message": "Comment not found."}, 404

        return comment.json(), 201

    def put(self, comment_id):
        data = self.parser.parse_args()

        comment = CommentModel.find_by_id(comment_id)

        if comment is None:
            return {"message": "Comment not found."}, 404

        try:
            comment.update(**data)
        except:
            return {"message": "An error occurred while updating Comment."}, 500

        return comment.json(), 200

    def delete(self, comment_id):
        comment = CommentModel.find_by_id(comment_id)

        if comment is None:
            return {"message": "Comment not found."}, 404

        try:
            comment.delete()
        except:
            return {"message": "An error occurred while deleting Comment."}, 500

        return {"message": "Comment deleted."}, 200


class CommentList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        required=True,
                        help="A title must be provided.")
    parser.add_argument('content',
                        required=True,
                        help="A content must be provided.")
    parser.add_argument('course_id',
                        required=True,
                        help="A course id must be provided.")
    parser.add_argument('author_id',
                        required=True,
                        help="An author id must be provided.")

    def get(self):
        comments = CommentModel.query.all()
        return [comment.json() for comment in comments]

    def post(self):
        data = self.parser.parse_args()

        comment = CommentModel(**data)
        try:
            comment.save()
        except:
            return {"message": "An error occurred while inserting Comment."}, 500

        return comment.json(), 201
