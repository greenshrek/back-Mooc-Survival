from flask_restful import Resource, reqparse
from models.course import CourseModel


class Course(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('title')
    parser.add_argument('content')

    def get(self, course_id):
        course = CourseModel.find_by_id(course_id)

        if course is None:
            return {"message": "Course not found."}, 404

        return course.json(), 201

    def put(self, course_id):
        data = self.parser.parse_args()

        course = CourseModel.find_by_id(course_id)

        if course is None:
            return {"message": "Course not found."}, 404

        try:
            course.update(**data)
        except:
            return {"message": "An error occured while updating Course."}, 500

        return course.json(), 200

    def delete(self, course_id):
        course = CourseModel.find_by_id(course_id)

        if course is None:
            return {"message": "Course not found."}, 404

        try:
            course.delete()
        except:
            return {"message": "An error occured while deleting Course."}, 500

        return {"message": "Course deleted."}, 200


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
            course.save()
        except:
            return {"message": "An error occured while inserting Course"}, 500

        return course.json(), 201
