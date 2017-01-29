from flask_restful import Resource, reqparse
from models.badge import BadgeModel


class Badge(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name')
    parser.add_argument('picture')

    def get(self, course_id, badge_id):
        badge = BadgeModel.find_by_id(badge_id)

        if badge is None:
            return {"message": "No badge found."}, 404

        return badge.json(), 200

    def put(self, course_id, badge_id):
        data = self.parser.parse_args()

        badge = BadgeModel.find_by_id(badge_id)

        if badge is None:
            return {"message": "No badge found."}, 404

        try:
            badge.update(**data)
        except:
            return {"message": "An error occured while updating Badge."}, 500

        return badge.json(), 200

    def delete(self, course_id, badge_id):
        badge = BadgeModel.find_by_id(badge_id)

        if badge is None:
            return {"message": "No badge found."}, 404

        try:
            badge.delete()
        except:
            return {"message": "An error occured while deleting Badge."}, 500

        return {"message": "Badge deleted."}, 200


class BadgeList(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        required=True,
                        help="A name must be provided.")
    parser.add_argument('student_id',
                        required=True,
                        help="A course_id must be provided.")
    parser.add_argument('picture')

    def get(self, course_id):
        badges = BadgeModel.find_by_course(course_id)

        return {"badges": [badge.json() for badge in badges]}

    def post(self, course_id):
        data = self.parser.parse_args()
        data['course_id'] = course_id

        badge = BadgeModel(**data)
        try:
            badge.save()
        except:
            return {"message": "An error occured while inserting Badge."}, 500

        return badge.json(), 201
