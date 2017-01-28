from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand

from models.user import UserModel, RoleModel
from models.course import CourseModel
from models.category import CategoryModel
from models.comment import CommentModel
from models.rating import RatingModel
from models.badge import BadgeModel
from models.chapter import ChapterModel
from models.quiz import QuizModel
from models.question import QuestionModel
from models.answer import AnswerModel
from models.score import ScoreModel

from app import create_app
from db import db

app = create_app()

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('runserver', Server(port=5555))
manager.add_command('db', MigrateCommand)

@manager.command
def test_db():
    student = RoleModel('student')
    instructor = RoleModel('instructor')
    db.session.add_all([student, instructor])
    db.session.commit()
    bart = UserModel('bart', 'bart', 'bart', 'student')
    lisa = UserModel('lisa', 'lisa', 'lisa', 'student')
    millhouse = UserModel('millhouse', 'millhouse', 'millhouse', 'student')
    edna = UserModel('edna', 'edna', 'edna', 'instructor')
    simour = UserModel('simour', 'simour', 'simour', 'instructor')
    db.session.add_all([bart, lisa, millhouse, edna, simour])
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
    db.session.add_all([maths, english])
    db.session.commit()
    math_course = CourseModel('mathematics', 'basic operations', simour.id, maths.id)
    english_course = CourseModel('english', 'grammar', edna.id, english.id)
    db.session.add_all([math_course, english_course])
    db.session.commit()
    math_course.register_student(bart.id)
    math_course.register_student(lisa.id)
    english_course.register_student(lisa.id)
    english_course.register_student(millhouse.id)
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
    chapter1 = ChapterModel('adds', '2 + 2 = 4', 1, math_course.id)
    chapter2 = ChapterModel('subs', '2 - 2 = 0', 2, math_course.id)
    db.session.add_all([chapter1, chapter2])
    db.session.commit()
    quiz1 = QuizModel('first grade', 1, math_course.id)
    quiz2 = QuizModel('second grade', 2, math_course.id)
    db.session.add(quiz1)
    db.session.add(quiz2)
    db.session.commit()
    question1 = QuestionModel('1 + 1?', 1, 2, quiz1.id)
    db.session.add(question1)
    db.session.commit()
    answer1 = AnswerModel('0', 1, question1.id)
    db.session.add(answer1)
    answer2 = AnswerModel('2', 2, question1.id)
    db.session.add(answer2)
    question2 = QuestionModel('3 - 1?', 2, 1, quiz1.id)
    db.session.add(question2)
    answer3 = AnswerModel('2', 1, question2.id)
    db.session.add(answer3)
    answer4 = AnswerModel('4', 2, question2.id)
    db.session.add(answer4)
    db.session.commit()
    print('::: test chapters and quizzes and questions and answers ::: ok')
    ###################
    print('chapters in math_course')
    for chapter in math_course.chapters:
        print('>>> {}'.format(chapter.title))
    print('quizzes in math_course')
    for quiz in math_course.quizzes:
        print('>>> {}'.format(quiz.title))
    print('questions in quiz1')
    for question in quiz1.questions:
        print('>>> {}'.format(question.question))
    print('answers in question1')
    for answer in question1.answers:
        print('>>> {}'.format(answer.answer))
    print('for question1 the good answer is number {}'.format(question1.good_answer))
    current_question = question1.question
    good_answer = AnswerModel.query.filter_by(number=question1.good_answer).first()
    print('question: {} | response: {}'.format(current_question, good_answer.answer))
    ###################
    comment1 = CommentModel('hay caramba', 'hay caramba', math_course.id, bart.id)
    comment2 = CommentModel('retention', 'retention', math_course.id, simour.id)
    comment3 = CommentModel('eat my short', 'eat my short', math_course.id, bart.id)
    db.session.add_all([comment1, comment2, comment3])
    db.session.commit()
    rate1 = RatingModel(5, english_course.id, lisa.id)
    rate2 = RatingModel(3, english_course.id, millhouse.id)
    db.session.add_all([rate1, rate2])
    db.session.commit()
    print('::: test comments and ratings ::: ok')
    ###################
    print('comments in math_course')
    for comment in math_course.comments:
        print('>>> {} by {}'.format(comment.title, comment.author.username))
    print('ratings in english_course')
    for rate in english_course.ratings:
        print('>>> {}/5 by {}'.format(rate.rate, rate.author.username))
    ###################
    score = ScoreModel(2, 2, lisa.id, quiz1.id)
    db.session.add(score)
    db.session.commit()
    badge = BadgeModel('honor', math_course.id, lisa.id)
    db.session.add(badge)
    db.session.commit()
    print('::: test scores and badges ::: ok')
    ###################
    print('badges earned by lisa')
    for badge in lisa.badges:
        print('>>> {}'.format(badge.name))
    print('scores in quiz1')
    for score in quiz1.scores:
        print('>>> {} by {}'.format(score.score, score.student.username))
    ###################

if __name__ == '__main__':
    manager.run()
