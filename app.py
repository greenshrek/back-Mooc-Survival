import os

from flask import Flask
from flask_restful import Api, Resource

from resources.course import CourseList, Course
from resources.user import UserList, User
from resources.category import CategoryList, Category
from resources.comment import CommentList, Comment
from resources.chapter import ChapterList, Chapter
from resources.quiz import QuizList, Quiz
from resources.question import QuestionList, Question
from resources.answer import AnswerList, Answer

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    from db import db
    db.init_app(app)

    api = Api(app)
    # users
    api.add_resource(UserList, '/users')
    api.add_resource(User, '/users/<int:user_id>')
    # categories
    api.add_resource(CategoryList, '/categories')
    api.add_resource(Category, '/categories/<int:category_id>')
    # courses
    api.add_resource(CourseList, '/courses')
    api.add_resource(Course, '/courses/<int:course_id>')
    # chapters
    api.add_resource(Chapter, '/courses/<int:course_id>/chapters/<int:chapter_id>')
    api.add_resource(ChapterList, '/courses/<int:course_id>/chapters')
    # quizzes
    api.add_resource(Quiz, '/courses/<int:course_id>/quizzes/<int:quiz_id>')
    api.add_resource(QuizList, '/courses/<int:course_id>/quizzes')
    # questions
    api.add_resource(Question, '/quizzes/<int:quiz_id>/questions/<int:question_id>')
    api.add_resource(QuestionList, '/quizzes/<int:quiz_id>/questions')
    # answers
    api.add_resource(Answer, '/questions/<int:question_id>/answers/<int:answer_id>')
    api.add_resource(AnswerList, '/questions/<int:question_id>/answers')
    # comments
    api.add_resource(CommentList, '/comments')
    api.add_resource(Comment, '/comments/<int:comment_id>')

    return app
