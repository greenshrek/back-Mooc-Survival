from models.course import CourseModel

def steps_count(course_id):
    course = CourseModel.find_by_id(course_id)

    steps_number = 0
    for chapter in course.chapters:
        steps_number += 1
    for quiz in course.quizzes:
        steps_number += 1

    return steps_number

def update_steps_number(course_id):
    course = CourseModel.find_by_id(course_id)

    steps_number = 0
    for chapter in course.chapters:
        steps_number += 1
    for quiz in course.quizzes:
        steps_number += 1

    for step in course.steps:
        step.final_step = steps_number

    db.session.commit()
