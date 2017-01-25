from flask_restful import Resource
from models.course import CourseModel


class CourseList(Resource):
    def get(self):
        courses = CourseModel.query.all()
        return {"courses": [course.json() for course in courses]}
