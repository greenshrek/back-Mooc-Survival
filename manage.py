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
    category = CategoryModel('unexpected')
    course = CourseModel(
        'survive to megan fox',
        'Megan Fox want to perform a marathon of sex with you.\
        How could you prepare for this?',
        user1, category)
    comment = CommentModel(
        'no one can survive to megan fox dumbass!',
        course, user2)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(category)
    db.session.add(course)
    db.session.add(comment)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
