from flask_restful import Resource, reqparse
from models.course import CourseModel


class CourseList(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        required=True,
                        help="A title must be provided.")
    parser.add_argument('content',
                        required=True,
                        help="A content must be provided.")
    parser.add_argument('author_id',
                        required=True,
                        help="An author id must be provided.")
    parser.add_argument('category_id',
                        required=True,
                        help="A category id must be provided.")

    def get(self):
        courses = CourseModel.query.all()
        return {"courses": [course.json() for course in courses]}

    def post(self):
        data = self.parser.parse_args()

        if CourseModel.query.filter_by(title=data['title']).first():
            msg = "A course with title:'{}' already exists.".format(
                data['title'])
            return {"message": msg}, 400

        course = CourseModel(**data)
        try:
            course.save_to_db()
        except:
            return {"message": "An error occured while inserting Course"}, 500

        return course.json(), 201
