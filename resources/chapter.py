from flask_restful import Resource, reqparse
from models.chapter import ChapterModel

parser = reqparse.RequestParser()
parser.add_argument('title',
                    required=True,
                    help="A title must be provided.")
parser.add_argument('content',
                    required=True,
                    help="A content must be provided.")
parser.add_argument('number',
                    type=int,
                    required=True,
                    help="A number must be provided.")

class Chapter(Resource):

    def get(self, course_id, chapter_id):
        chapter = ChapterModel.find_by_id(chapter_id)

        if chapter is None:
            return {"message": "No chapter found."}, 404

        return chapter.json(), 200

    def put(self, course_id, chapter_id):
        data = parser.parse_args()
        data['course_id'] = course_id


        chapter = ChapterModel.find_by_id(chapter_id)

        if chapter is None:
            new_chapter = ChapterModel(**data)
            try:
                new_chapter.save()

                return new_chapter.json(), 201
            except:
                return {"message": "An error occurred while updating Chapter."}, 500

        try:
            chapter.update(**data)
        except:
            return {"message": "An error occurred while updating Chapter."}, 500

        return chapter.json(), 200

    def delete(self, course_id, chapter_id):
        chapter = ChapterModel.find_by_id(chapter_id)

        if chapter is None:
            return {"message": "No chapter found."}, 404

        try:
            chapter.delete()
        except:
            return {"message": "An error occurred while deleting Chapter."}, 500

        return {"message": "Chapter deleted."}, 200


class ChapterList(Resource):

    def get(self, course_id):
        chapters = ChapterModel.find_by_course(course_id)

        if chapters is None:
            return {"message": "No chapters found for this course."}, 404

        return [chapter.json() for chapter in chapters], 200

    def post(self, course_id):
        data = parser.parse_args()
        data['course_id'] = course_id

        chapter = ChapterModel(**data)
        try:
            chapter.save()
        except:
            return {"message": "An error occurred while inserting Chapter."}, 500

        return chapter.json(), 201
