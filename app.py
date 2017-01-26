import os

from flask import Flask
from flask_restful import Api, Resource

# from resources.course import CourseList, Course
# from resources.user import UserList, User
# from resources.category import CategoryList, Category
# from resources.comment import CommentList, Comment

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    from db import db
    db.init_app(app)

    # api = Api(app)
    # api.add_resource(CourseList, '/courses')
    # api.add_resource(Course, '/courses/<int:course_id>')
    # api.add_resource(UserList, '/users')
    # api.add_resource(User, '/users/<int:user_id>')
    # api.add_resource(CategoryList, '/categories')
    # api.add_resource(Category, '/categories/<int:category_id>')
    # api.add_resource(CommentList, '/comments')
    # api.add_resource(Comment, '/comments/<int:comment_id>')

    return app
