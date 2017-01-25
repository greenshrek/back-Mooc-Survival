from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand

from models.user import UserModel
from models.course import CourseModel
from models.category import CategoryModel
from models.comment import CommentModel

from app import create_app
from db import db

app = create_app()

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('runserver', Server(port=5555))
manager.add_command('db', MigrateCommand)

@manager.command
def populatedb():
    user1 = UserModel('bob', '1234', 'bob@example.com')
    user2 = UserModel('bill', '1234', 'bill@example.com')
    category1 = CategoryModel('forest')
    category2 = CategoryModel('desert')
    course1 = CourseModel(
        'survive in forest',
        'How to survive in forest',
        1, 1)
    course2 = CourseModel(
        'survive in desert',
        'How to survive in desert',
        1, 2)
    course3 = CourseModel(
        'find water',
        'How to find water in desert',
        1, 2)
    comment = CommentModel(
        'Learn to start fire first',
        1, 2)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(category1)
    db.session.add(category2)
    db.session.add(course1)
    db.session.add(course2)
    db.session.add(course3)
    db.session.add(comment)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
