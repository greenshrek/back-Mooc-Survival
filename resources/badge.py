from flask_restful import Resource, reqparse
from models.badge import BadgeModel
from models.user import UserModel

parser = reqparse.RequestParser()
parser.add_argument('name',
                    required=True,
                    help="A name must be provided.")
parser.add_argument('course_id',
                    type=int,
                    required=True,
                    help="A course_id must be provided.")
parser.add_argument('picture')


class Badge(Resource):

    def get(self, student_id, badge_id):
        badge = BadgeModel.find_by_id(badge_id)

        if badge is None:
            return {"message": "No badge found."}, 404

        return badge.json(), 200

    def put(self, student_id, badge_id):
        data = parser.parse_args()

        badge = BadgeModel.find_by_id(badge_id)

        if badge is None:
            data['student_id'] = student_id

            new_badge = BadgeModel(**data)
            try:
                new_badge.save()

                return new_badge.json(), 201
            except:
                return {"message": "An error occurred while inserting Badge."}

        try:
            badge.update(**data)
        except:
            return {"message": "An error occurred while updating Badge."}, 500

        return badge.json(), 200

    def delete(self, student_id, badge_id):
        badge = BadgeModel.find_by_id(badge_id)

        if badge is None:
            return {"message": "No badge found."}, 404

        try:
            badge.delete()
        except:
            return {"message": "An error occurred while deleting Badge."}, 500

        return {"message": "Badge deleted."}, 200


class BadgeList(Resource):

    def get(self, student_id):
        student = UserModel.find_by_id(student_id)
        badges = [badge for badge in student.badges]

        return [badge.json() for badge in badges]

    def post(self, student_id):
        data = parser.parse_args()
        data['student_id'] = student_id

        badge = BadgeModel(**data)
        try:
            badge.save()
        except:
            return {"message": "An error occurred while inserting Badge."}, 500

        return badge.json(), 201
