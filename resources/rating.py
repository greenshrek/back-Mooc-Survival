from flask_restful import Resource, reqparse
from models.rating import RatingModel

parser = reqparse.RequestParser()
parser.add_argument('rate',
                    type=int,
                    required=True,
                    help="A name must be provided.")
parser.add_argument('author_id',
                    type=int,
                    required=True,
                    help="A author_id must be provided.")

class Rating(Resource):

    def get(self, course_id, rating_id):
        rating = RatingModel.find_by_id(rating_id)

        if rating is None:
            return {"message": "No rating found."}, 404

        return rating.json(), 200

    def put(self, course_id, rating_id):
        data = self.parser.parse_args()
        data['course_id'] = course_id

        rating = RatingModel.find_by_id(rating_id)

        if rating is None:
            new_rating = RatingModel(**data)
            try:
                new_rating.save()

                return new_rating.json(), 201
            except:
                return {"message": "An error occurred while updating Rating."}, 500

        try:
            rating.update(**data)
        except:
            return {"message": "An error occurred while updating Rating."}, 500

        return rating.json(), 200

    def delete(self, course_id, rating_id):
        rating = RatingModel.find_by_id(rating_id)

        if rating is None:
            return {"message": "No rating found."}, 404

        try:
            rating.delete()
        except:
            return {"message": "An error occurred while deleting Rating."}, 500

        return {"message": "Rating deleted."}, 200


class RatingList(Resource):

    def get(self, course_id):
        ratings = RatingModel.find_by_course(course_id)

        return [rating.json() for rating in ratings], 200

    def post(self, course_id):
        data = self.parser.parse_args()
        data['course_id'] = course_id

        rating = RatingModel(**data)
        try:
            rating.save()
        except:
            return {"message": "An error occurred while inserting Rating."}, 500

        return rating.json(), 201
