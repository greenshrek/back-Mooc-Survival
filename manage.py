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
def new_test_db():
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
    math_course = CourseModel('mathematics', 'basic operations', 'simour', 'maths')
    english_course = CourseModel('english', 'grammar', 'edna', 'english')
    db.session.add_all([math_course, english_course])
    db.session.commit()
    math_course.register_student('bart')
    math_course.register_student('lisa')
    english_course.register_student('lisa')
    english_course.register_student('millhouse')
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


@manager.command
def test_db():
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
    chapter1 = ChapterModel('adds', '2 + 2 = 4', 1)
    chapter2 = ChapterModel('subs', '2 - 2 = 0', 2)
    quiz = QuizModel('first grade', 1)
    question1 = QuestionModel('1 + 1?', 1, 2)
    answer1 = AnswerModel('0', 1)
    answer2 = AnswerModel('2', 2)
    question2 = QuestionModel('3 - 1?', 2, 1)
    answer3 = AnswerModel('2', 1)
    answer4 = AnswerModel('4', 2)
    lisa_score = ScoreModel(2, 2)
    db.session.add_all([chapter1, chapter2, quiz, question1, question2, answer1, answer2, answer3, answer4, lisa_score])
    math_course.chapters.append(chapter1)
    math_course.chapters.append(chapter2)
    math_course.quizzes.append(quiz)
    quiz.questions.append(question1)
    quiz.questions.append(question2)
    question1.answers.append(answer1)
    question1.answers.append(answer2)
    question2.answers.append(answer3)
    question2.answers.append(answer4)
    lisa.scores.append(lisa_score)
    quiz.scores.append(lisa_score)
    db.session.commit()
    print('::: test chapters and quizzes and questions and answers and scores ::: ok')
    ###################
    print('chapters in math_course')
    for chapter in math_course.chapters:
        print('>>> {}'.format(chapter.title))
    print('quizzes in math_course')
    for quiz in math_course.quizzes:
        print('>>> {}'.format(quiz.title))
    print('questions in quiz')
    for question in quiz.questions:
        print('>>> {}'.format(question.question))
    print('answers in question1')
    for answer in question1.answers:
        print('>>> {}'.format(answer.answer))
    print('for question1 the good answer is number {}'.format(question1.good_answer))
    current_question = question1.question
    good_answer = AnswerModel.query.filter_by(number=question1.good_answer).first()
    print('question: {} | response: {}'.format(current_question, good_answer.answer))
    print('lisa scores')
    for score in lisa.scores:
        print('>>> {}/{}'.format(score.score, score.max_score))
    ###################


if __name__ == '__main__':
    manager.run()
