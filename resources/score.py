from flask_restful import Resource, reqparse
from models.score import ScoreModel


class Score(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('score')
    parser.add_argument('max_score')

    def get(self, quiz_id, student_id, score_id):
        score = ScoreModel.find_by_id(score_id)

        if score is None:
            return {"message": "No score found."}, 404

        return score.json(), 200

    def put(self, quiz_id, student_id, score_id):
        data = self.parser.parse_args()

        score = ScoreModel.find_by_id(score_id)

        if score is None:
            return {"message": "No score found."}, 404

        try:
            score.update(**data)
        except:
            return {"message": "An error occured while updating Score."}, 500

        return score.json(), 200

    def delete(self, quiz_id, student_id, score_id):
        score = ScoreModel.find_by_id(score_id)

        if score is None:
            return {"message": "No score found."}, 404

        try:
            score.delete()
        except:
            return {"message": "An error occured while deleting Score."}, 500

        return {"message": "Score deleted."}, 200


class ScoreList(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('score',
                        required=True,
                        help="A score must be provided.")
    parser.add_argument('max_score',
                        required=True,
                        help="A max_score must be provided.")

    def get(self, quiz_id, student_id):
        scores = ScoreModel.query.all()

        return {"scores": [score.json() for score in scores]}

    def post(self, quiz_id, student_id):
        data = self.parser.parse_args()
        data['quiz_id'] = quiz_id
        data['student_id'] = student_id

        score = ScoreModel(**data)
        try:
            score.save()
        except:
            return {"message": "An error occured while inserting Score."}, 500

        return score.json(), 201
