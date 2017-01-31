from flask_restful import Resource, reqparse
from models.step import StepModel

parser = reqparse.RequestParser()
parser.add_argument('current_step',
                    type=int,
                    required=True,
                    help="A current_step must be provided.")


class Step(Resource):

    def put(self, student_id, course_id, step_id):
        data = parser.parse_args()
        data['student_id'] = student_id
        data['course_id'] = course_id

        step = StepModel.find_by_id(step_id)

        if step is None:
            new_step = StepModel(**data)
            try:
                new_step.save()
            except:
                return {"message": "An error occurred while inserting Step."}, 500

        if data['current_step'] < step.current_step:
            data['current_step'] = step.current_step

        try:
            step.update(**data)
        except:
            return {"message": "An error occurred while updating Step."}, 500

        return step.json(), 200
