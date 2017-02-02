from flask_restful import Resource, reqparse
from models.quiz import QuizModel
from helpers.step import update_steps_number

parser = reqparse.RequestParser()
parser.add_argument('title',
                    required=True,
                    help="A title must be provided.")
parser.add_argument('number',
                    type=int,
                    required=True,
                    help="A number must be provided.")

class Quiz(Resource):

    def get(self, course_id, quiz_id):
        quiz = QuizModel.find_by_id(quiz_id)

        if quiz is None:
            return {"message": "No quiz found."}, 404

        return quiz.json(), 200

    def put(self, course_id, quiz_id):
        data = parser.parse_args()
        data['course_id'] = course_id

        quiz = QuizModel.find_by_id(quiz_id)

        if quiz is None:
            new_quiz = QuizModel(**data)
            try:
                new_quiz.save()

                return new_quiz.json(), 201
            except:
                return {"message": "An error occurred while inserting Quiz."}, 500

        try:
            quiz.update(**data)
        except:
            return {"message": "An error occurred while updating Quiz."}, 500

        return quiz.json(), 200

    def delete(self, course_id, quiz_id):
        quiz = QuizModel.find_by_id(quiz_id)

        if quiz is None:
            return {"message": "No quiz found."}, 404

        try:
            quiz.delete()
        except:
            return {"message": "An error occurred while deleting Quiz."}, 500

        update_steps_number(course_id)

        return {"message": "Quiz deleted."}, 200


class QuizList(Resource):

    def get(self, course_id):
        quizzes = QuizModel.find_by_course(course_id)

        if quizzes is None:
            return {"message": "No quizzes found for this course."}, 404

        return [quiz.json() for quiz in quizzes], 200

    def post(self, course_id):
        data = parser.parse_args()
        data['course_id'] = course_id

        quiz = QuizModel(**data)
        try:
            quiz.save()
        except:
            return {"message": "An error occurred while inserting Quiz."}, 500

        update_steps_number(course_id)

        return quiz.json(), 201
