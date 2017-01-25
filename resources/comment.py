from flask_restful import Resource, reqparse
from models.comment import CommentModel


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
