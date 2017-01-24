import os

from flask import Flask
from flask_restful import Api, Resource

from resources.course import CourseList
from resources.user import UserList
from resources.category import CategoryList
from resources.comment import CommentList

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    from db import db
    db.init_app(app)

    api = Api(app)
    api.add_resource(CourseList, '/courses')
    api.add_resource(UserList, '/users')
    api.add_resource(CategoryList, '/categories')
    api.add_resource(CommentList, '/comments')

    return app
