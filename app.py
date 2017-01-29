import os

from flask import Flask
from flask_restful import Api, Resource
# import resources
from resources.course import CourseList, Course
from resources.user import UserList, User
from resources.category import CategoryList, Category
from resources.comment import CommentList, Comment
from resources.chapter import ChapterList, Chapter
from resources.quiz import QuizList, Quiz
from resources.question import QuestionList, Question
from resources.answer import AnswerList, Answer
from resources.score import ScoreList, Score
from resources.badge import BadgeList, Badge
from resources.rating import RatingList, Rating

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    from db import db
    db.init_app(app)

    api = Api(app)
    # users
    api.add_resource(User, '/users/<int:user_id>')
    api.add_resource(UserList, '/users')
    # categories
    api.add_resource(Category, '/categories/<int:category_id>')
    api.add_resource(CategoryList, '/categories')
    # courses
    api.add_resource(Course, '/courses/<int:course_id>')
    api.add_resource(CourseList, '/courses')
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
    api.add_resource(Comment, '/comments/<int:comment_id>')
    api.add_resource(CommentList, '/comments')
    # scores
    api.add_resource(Score, '/quizzes/<int:quiz_id>/students/<int:student_id>/scores/<int:score_id>')
    api.add_resource(ScoreList, '/quizzes/<int:quiz_id>/students/<int:student_id>/scores')
    # badges
    api.add_resource(Badge, '/courses/<int:course_id>/badges/<int:badge_id>')
    api.add_resource(BadgeList, '/courses/<int:course_id>/badges')
    # ratings
    api.add_resource(Rating, '/courses/<int:course_id>/ratings/<int:rating_id>')
    api.add_resource(RatingList, '/courses/<int:course_id>/ratings')

    return app
