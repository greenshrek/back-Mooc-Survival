from flask_restful import Resource, reqparse
from models.score import ScoreModel

parser = reqparse.RequestParser()
parser.add_argument('score',
                    required=True,
                    help="A score must be provided.")
parser.add_argument('max_score',
                    required=True,
                    help="A max_score must be provided.")

class Score(Resource):

    def get(self, quiz_id, score_id):
        score = ScoreModel.find_by_id(score_id)

        if score is None:
            return {"message": "No score found."}, 404

        return score.json(), 200

    def put(self, quiz_id, score_id):
        data = parser.parse_args()

        score = ScoreModel.find_by_id(score_id)

        if score is None:
            new_score = ScoreModel(**data)
            try:
                new_score.save()

                return new_score.json(), 201
            except:
                return {"message": "An error occurred while inserting Score."}, 500
        try:
            score.update(**data)
        except:
            return {"message": "An error occurred while updating Score."}, 500

        return score.json(), 200

    def delete(self, quiz_id, score_id):
        score = ScoreModel.find_by_id(score_id)

        if score is None:
            return {"message": "No score found."}, 404

        try:
            score.delete()
        except:
            return {"message": "An error occurred while deleting Score."}, 500

        return {"message": "Score deleted."}, 200


class ScoreList(Resource):

    def get(self, quiz_id):
        scores = ScoreModel.find_by_quiz(quiz_id)

        return [score.json() for score in scores], 200

    def post(self, quiz_id):
        data = parser.parse_args()
        data['quiz_id'] = quiz_id

        score = ScoreModel(**data)
        try:
            score.save()
        except:
            return {"message": "An error occurred while inserting Score."}, 500

        return score.json(), 201
