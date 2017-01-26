from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand

from models.user import StudentModel, InstructorModel
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
    # student = StudentModel('jane', 'jane', 'jane@company.com')
    # instructor = InstructorModel('john', 'john', 'john@example.com')
    # category = CategoryModel('forest')
    # course = CourseModel('forest', 'grand forest', 1)
    # db.session.add(student)
    # db.session.add(instructor)
    # db.session.add(category)
    # db.session.add(course)
    # course.students.append(student)
    # db.session.add(course)
    # db.session.commit()
    pass

if __name__ == '__main__':
    manager.run()
