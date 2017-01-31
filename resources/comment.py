from flask_restful import Resource, reqparse
from models.comment import CommentModel

parser = reqparse.RequestParser()
parser.add_argument('title',
                    required=True,
                    help="A title must be provided.")
parser.add_argument('content',
                    required=True,
                    help="A content must be provided.")
parser.add_argument('author_id',
                    type=int,
                    required=True,
                    help="An author id must be provided.")

class Comment(Resource):

    def get(self, course_id, comment_id):
        comment = CommentModel.find_by_id(comment_id)

        if comment is None:
            return {"message": "Comment not found."}, 404

        return comment.json(), 201

    def put(self, course_id, comment_id):
        data = parser.parse_args()
        data['course_id'] = course_id

        comment = CommentModel.find_by_id(comment_id)

        if comment is None:
            new_comment = CommentModel(**data)
            try:
                new_comment.save()

                return new_comment.json(), 201
            except:
                return {"message": "An error occurred while inserting Comment."}, 500
        try:
            comment.update(**data)
        except:
            return {"message": "An error occurred while updating Comment."}, 500

        return comment.json(), 200

    def delete(self, course_id, comment_id):
        comment = CommentModel.find_by_id(comment_id)

        if comment is None:
            return {"message": "Comment not found."}, 404

        try:
            comment.delete()
        except:
            return {"message": "An error occurred while deleting Comment."}, 500

        return {"message": "Comment deleted."}, 200


class CommentList(Resource):

    def get(self, course_id):
        comments = CommentModel.find_by_course(course_id)

        return {"comments": [comment.json() for comment in comments]}, 200

    def post(self, course_id):
        data = parser.parse_args()
        data['course_id'] =course_id

        comment = CommentModel(**data)
        try:
            comment.save()
        except:
            return {"message": "An error occurred while inserting Comment."}, 500

        return comment.json(), 201
