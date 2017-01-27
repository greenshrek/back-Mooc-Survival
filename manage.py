from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand

from models.user import UserModel, RoleModel
from models.course import CourseModel
from models.category import CategoryModel
from models.comment import CommentModel
from models.rating import RatingModel
from models.badge import BadgeModel

from app import create_app
from db import db

app = create_app()

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('runserver', Server(port=5555))
manager.add_command('db', MigrateCommand)

@manager.command
def populatedb():
    student = RoleModel('student')
    instructor = RoleModel('instructor')
    bart = UserModel('bart', 'bart', 'bart')
    lisa = UserModel('lisa', 'lisa', 'lisa')
    millhouse = UserModel('millhouse', 'millhouse', 'millhouse')
    edna = UserModel('edna', 'edna', 'edna')
    simour = UserModel('simour', 'simour', 'simour')
    db.session.add_all([student, instructor, bart, lisa, millhouse, edna, simour])
    db.session.commit()
    student.users.append(bart)
    student.users.append(lisa)
    student.users.append(millhouse)
    instructor.users.append(edna)
    instructor.users.append(simour)
    db.session.commit()
    print('::: test roles and users ::: ok')
    ###################
    print('students')
    for student in student.users:
        print('>>> {}'.format(student.username))
    print('instructors')
    for instructor in instructor.users:
        print('>>> {}'.format(instructor.username))
    ###################
    maths = CategoryModel('maths')
    english = CategoryModel('english')
    math_course = CourseModel('mathematics', 'basic operations')
    english_course = CourseModel('english', 'grammar')
    db.session.add_all([maths, english, math_course, english_course])
    db.session.commit()
    maths.courses.append(math_course)
    english.courses.append(english_course)
    bart.enrolled_courses.append(math_course)
    millhouse.enrolled_courses.append(english_course)
    lisa.enrolled_courses.append(math_course)
    lisa.enrolled_courses.append(english_course)
    edna.published_courses.append(english_course)
    simour.published_courses.append(math_course)
    db.session.commit()
    print('::: test categories and courses ::: ok')
    ###################
    print('students enrolled in math')
    for student in math_course.students:
        print('>>> {}'.format(student.username))
    print('author of math_course')
    print('>>> {}'.format(math_course.author.username))
    print('edna published courses')
    for course in edna.published_courses:
        print('>>> {} - {}'.format(course.title, course.category.name))
    ###################
    bart_cmt = CommentModel('hay caramba', 'eat my short')
    db.session.add(bart_cmt)
    bart.comments.append(bart_cmt)
    math_course.comments.append(bart_cmt)
    db.session.commit()
    simour_cmt = CommentModel('punishment', '2 hours of detention')
    db.session.add(simour_cmt)
    simour.comments.append(simour_cmt)
    math_course.comments.append(simour_cmt)
    db.session.commit()
    english_rate = RatingModel(5)
    db.session.add(english_rate)
    lisa.ratings.append(english_rate)
    english_course.ratings.append(english_rate)
    db.session.commit()
    math_badge = BadgeModel('mathematician')
    db.session.add(math_badge)
    db.session.commit()
    lisa.badges.append(math_badge)
    math_badge.course = math_course
    db.session.commit()
    print('::: test  comments and ratings and badges ::: ok')
    ###################
    print('comments in math')
    for comment in math_course.comments:
        print('>>> {}'.format(comment.title))
    print('ratings in english_course')
    for rating in english_course.ratings:
        print('>>> {}/5'.format(rating.rate))
    print('badges in lisa')
    for badge in lisa.badges:
        print('>>> {}'.format(badge.name))
    print('badge course and badge student')
    for student in math_badge.students:
        print('>>> {} badge earned by {}'.format(math_badge.name, student.username))
    ###################


if __name__ == '__main__':
    manager.run()
