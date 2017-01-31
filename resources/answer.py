from flask_restful import Resource, reqparse
from models.answer import AnswerModel

parser = reqparse.RequestParser()
parser.add_argument('answer',
                    required=True,
                    help="A answer must be provided.")
parser.add_argument('number',
                    type=int,
                    required=True,
                    help="A number must be provided.")


class Answer(Resource):

    def get(self, question_id, answer_id):
        answer = AnswerModel.find_by_id(answer_id)

        if answer is None:
            return {"message": "No answer found."}, 404

        return answer.json(), 200

    def put(self, question_id, answer_id):
        data = parser.parse_args()
        data['question_id'] = question_id

        answer = AnswerModel.find_by_id(answer_id)

        if answer is None:
            new_answer = AnswerModel(**data)
            try:
                new_answer.save()

                return new_answer.json(), 201
            except:
                return {"message": "An error occurred while inserting Question."}, 500

        try:
            answer.update(**data)
        except:
            return {"message": "An error occurred while updating Question."}, 500

        return answer.json(), 200

    def delete(self, question_id, answer_id):
        answer = AnswerModel.find_by_id(answer_id)

        if answer is None:
            return {"message": "No answer found."}, 404

        try:
            answer.delete()
        except:
            return {"message": "An error occurred while deleting Question."}, 500

        return {"message": "Question deleted."}, 200


class AnswerList(Resource):

    def get(self, question_id):
        answers = AnswerModel.find_by_question(question_id)

        if answers is None:
            return {"message": "No answers found for this quiz."}, 404

        return [answer.json() for answer in answers], 200

    def post(self, question_id):
        data = parser.parse_args()
        data['question_id'] = question_id

        answer = AnswerModel(**data)
        try:
            answer.save()
        except:
            return {"message": "An error occurred while inserting Question."}, 500

        return answer.json(), 201
