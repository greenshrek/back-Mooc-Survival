from flask_restful import Resource, reqparse
from models.chapter import ChapterModel


class Chapter(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('title')
    parser.add_argument('content')
    parser.add_argument('number')

    def get(self, course_id, chapter_id):
        chapter = ChapterModel.find_by_id(chapter_id)

        if chapter is None:
            return {"message": "No chapter found."}, 404

        return chapter.json(), 200

    def put(self, course_id, chapter_id):
        data = self.parser.parse_args()

        chapter = ChapterModel.find_by_id(chapter_id)

        if chapter is None:
            return {"message": "No chapter found."}, 404

        try:
            chapter.update(**data)
        except:
            return {"message": "An error occured while updating Chapter."}, 500

        return chapter.json(), 200

    def delete(self, course_id, chapter_id):
        chapter = ChapterModel.find_by_id(chapter_id)

        if chapter is None:
            return {"message": "No chapter found."}, 404

        try:
            chapter.delete()
        except:
            return {"message": "An error occured while deleting Chapter."}, 500

        return {"message": "Chapter deleted."}, 200


class ChapterList(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        required=True,
                        help="A title must be provided.")
    parser.add_argument('content',
                        required=True,
                        help="A content must be provided.")
    parser.add_argument('number',
                        required=True,
                        help="A number must be provided.")

    def get(self, course_id):
        chapters = ChapterModel.find_by_course(course_id)

        if chapters is None:
            return {"message": "No chapters found for this course."}, 404

        return {"chapters": [chapter.json() for chapter in chapters]}, 200

    def post(self, course_id):
        data = self.parser.parse_args()
        data['course_id'] = course_id

        chapter = ChapterModel(**data)
        try:
            chapter.save()
        except:
            return {"message": "An error occured while inserting Chapter."}, 500

        return chapter.json(), 201
