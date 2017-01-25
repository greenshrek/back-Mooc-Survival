from flask_restful import Resource, reqparse
from models.comment import CommentModel


class Comment(Resource):

    parser = reqparse.RequestParser()

    def get(self, comment_id):
        comment = CommentModel.find_by_id(comment_id)

        if comment is None:
            return {"message": "Comment not found."}, 404

        return comment.json(), 201

    def delete(self, comment_id):
        comment = CommentModel.find_by_id(comment_id)

        if comment is None:
            return {"message": "Comment not found."}, 404

        try:
            comment.delete_from_db()
        except:
            return {"message": "An error occured while deleting Comment."}, 500

        return {"message": "Comment deleted."}, 200


class CommentList(Resource):
    parser = reqparse.RequestParser()
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
        return {"comments": [comment.json() for comment in comments]}

    def post(self):
        data = self.parser.parse_args()

        comment = CommentModel(**data)
        try:
            comment.save_to_db()
        except:
            return {"message": "An error occured while inserting Comment."}, 500

        return comment.json(), 201
