from flask_restful import Resource, reqparse
from models.quiz import QuizModel


class Quiz(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('title')
    parser.add_argument('number')

    def get(self, course_id, quiz_id):
        quiz = QuizModel.find_by_id(quiz_id)

        if quiz is None:
            return {"message": "No quiz found."}, 404

        return quiz.json(), 200

    def put(self, course_id, quiz_id):
        data = self.parser.parse_args()

        quiz = QuizModel.find_by_id(quiz_id)

        if quiz is None:
            return {"message": "No quiz found."}, 404

        try:
            quiz.update(**data)
        except:
            return {"message": "An error occured while updating Quiz."}, 500

        return quiz.json(), 200

    def delete(self, course_id, quiz_id):
        quiz = QuizModel.find_by_id(quiz_id)

        if quiz is None:
            return {"message": "No quiz found."}, 404

        try:
            quiz.delete()
        except:
            return {"message": "An error occured while deleting Quiz."}, 500

        return {"message": "Quiz deleted."}, 200


class QuizList(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        required=True,
                        help="A title must be provided.")
    parser.add_argument('number',
                        required=True,
                        help="A number must be provided.")

    def get(self, course_id):
        quizzes = QuizModel.find_by_course(course_id)

        if quizzes is None:
            return {"message": "No quizzes found for this course."}, 404

        return {"quizzes": [quiz.json() for quiz in quizzes]}, 200

    def post(self, course_id):
        data = self.parser.parse_args()
        data['course_id'] = course_id

        quiz = QuizModel(**data)
        try:
            quiz.save()
        except:
            return {"message": "An error occured while inserting Quiz."}, 500

        return quiz.json(), 201
