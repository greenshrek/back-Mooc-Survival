from flask_restful import Resource, reqparse
from models.question import QuestionModel

parser = reqparse.RequestParser()
parser.add_argument('question',
                    required=True,
                    help="A question must be provided.")
parser.add_argument('good_answer',
                    type=int,
                    required=True,
                    help="A good_answer must be provided.")
parser.add_argument('number',
                    type=int,
                    required=True,
                    help="A number must be provided.")


class Question(Resource):

    def get(self, quiz_id, question_id):
        question = QuestionModel.find_by_id(question_id)

        if question is None:
            return {"message": "No question found."}, 404

        return question.json(), 200

    def put(self, quiz_id, question_id):
        data = parser.parse_args()
        data['quiz_id'] = quiz_id

        question = QuestionModel.find_by_id(question_id)

        if question is None:
            new_question = QuestionModel(**data)
            try:
                new_question.save()

                return new_question.json(), 201
            except:
                return {"message": "An error occurred while inserting Question."}, 500

        try:
            question.update(**data)
        except:
            return {"message": "An error occurred while updating Question."}, 500

        return question.json(), 200

    def delete(self, quiz_id, question_id):
        question = QuestionModel.find_by_id(question_id)

        if question is None:
            return {"message": "No question found."}, 404

        try:
            question.delete()
        except:
            return {"message": "An error occurred while deleting Question."}, 500

        return {"message": "Question deleted."}, 200


class QuestionList(Resource):

    def get(self, quiz_id):
        questions = QuestionModel.find_by_quiz(quiz_id)

        if questions is None:
            return {"message": "No questions found for this quiz."}, 404

        return [question.json() for question in questions], 200

    def post(self, quiz_id):
        data = parser.parse_args()
        data['quiz_id'] = quiz_id

        question = QuestionModel(**data)
        try:
            question.save()
        except:
            return {"message": "An error occurred while inserting Question."}, 500

        return question.json(), 201
