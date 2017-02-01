import os

from flask import Flask
from flask_restful import Api, Resource
from flask_jwt import JWT
from security import authenticate, identity
# import resources
from resources.course import CourseList, Course
from resources.user import UserRegister, User, UserId
from resources.category import CategoryList, Category
from resources.comment import CommentList, Comment
from resources.chapter import ChapterList, Chapter
from resources.quiz import QuizList, Quiz
from resources.question import QuestionList, Question
from resources.answer import AnswerList, Answer
from resources.score import ScoreList, Score
from resources.badge import BadgeList, Badge
from resources.rating import RatingList, Rating
from resources.step import Step

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    from db import db
    db.init_app(app)

    # TODO: check resources: ratings, scores
    api = Api(app)

    jwt = JWT(app, authenticate, identity) # endpoint '/auth'

    # users
    api.add_resource(UserRegister, '/v1/register')
    api.add_resource(User, '/v1/users/<string:username>')
    api.add_resource(UserId, '/v1/users/<int:user_id>')
    # badges
    api.add_resource(BadgeList, '/v1/users/<int:student_id>/badges')
    api.add_resource(Badge, '/v1/users/<int:student_id>/badges/<int:badge_id>')
    # categories
    api.add_resource(CategoryList, '/v1/categories')
    api.add_resource(Category, '/v1/categories/<int:category_id>')
    # courses
    api.add_resource(CourseList, '/v1/courses')
    api.add_resource(Course, '/v1/courses/<int:course_id>')
    # chapters
    api.add_resource(ChapterList, '/v1/courses/<int:course_id>/chapters')
    api.add_resource(Chapter, '/v1/courses/<int:course_id>/chapters/<int:chapter_id>')
    # quizzes
    api.add_resource(QuizList, '/v1/courses/<int:course_id>/quizzes')
    api.add_resource(Quiz, '/v1/courses/<int:course_id>/quizzes/<int:quiz_id>')
    # comments
    api.add_resource(CommentList, '/v1/courses/<int:course_id>/comments')
    api.add_resource(Comment, '/v1/courses/<int:course_id>/comments/<int:comment_id>')
    # ratings
    api.add_resource(RatingList, '/v1/courses/<int:course_id>/ratings')
    api.add_resource(Rating, '/v1/courses/<int:course_id>/ratings/<int:rating_id>')
    # questions
    api.add_resource(QuestionList, '/v1/quizzes/<int:quiz_id>/questions')
    api.add_resource(Question, '/v1/quizzes/<int:quiz_id>/questions/<int:question_id>')
    # answers
    api.add_resource(AnswerList, '/v1/questions/<int:question_id>/answers')
    api.add_resource(Answer, '/v1/questions/<int:question_id>/answers/<int:answer_id>')
    # scores
    api.add_resource(ScoreList, '/v1/quizzes/<int:quiz_id>/scores')
    api.add_resource(Score, '/v1/quizzes/<int:quiz_id>/scores/<int:score_id>')
    # steps
    api.add_resource(Step, '/v1/users/<int:student_id>/courses/<int:course_id>/steps/<int:step_id>')

    return app
