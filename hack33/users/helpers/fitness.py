import ast
from hack33.users.models import (CourseClass,
                                 Teacher)

POINTS = 5


def is_any_empty_day(schedule):
    for k, v in schedule.items():
        if v == []:
            return True
    return False


def more_than_7_hours(schedule):
    for k, v in schedule.items():
        if len(v) > 7:
            return True
    return False


def less_than_2_hours(schedule):
    for k, v in schedule.items():
        if len(v) < 2:
            return True
    return False


def get_class_rating(week_schedule):
    ordered = True
    for day, schedule in week_schedule.items():
        for i in range(len(schedule) - 1):
            current = schedule[i]
            if current in schedule[i+1:len(schedule)]:
                if schedule[i] != schedule[i+1]:
                    ordered = False
                    break
    if ordered:
        return POINTS
    return 0


def give_rating_by_arrangement(schedule):
    schedule_rating = 0
    for c, week_schedule in schedule.items():
        class_rating = get_class_rating(week_schedule)
        schedule_rating += class_rating
    # print(schedule_rating)
    return schedule_rating


def check_teachers_schedule(schedule):
    result = 0
    teachers = Teacher.objects.all()
    for t in teachers:
        classes = {}
        teacher_classes = CourseClass.objects.get_teacher_classes(t)
        if not teacher_classes.exists():
            continue
        for t_class in teacher_classes:
            class_name = t_class.students.group_name
            course_name = t_class.course.name
            classes[class_name] = {
                "monday": get_course_indxes_by_day("monday", schedule, class_name, course_name),
                "tuesday": get_course_indxes_by_day("tuesday", schedule, class_name, course_name),
                "wednesday": get_course_indxes_by_day("wednesday", schedule, class_name, course_name),
                "thursday": get_course_indxes_by_day("thursday", schedule, class_name, course_name),
                "friday": get_course_indxes_by_day("friday", schedule, class_name, course_name)
            }
        result += check_for_conflixes(classes)
    return result


def get_course_indxes_by_day(day, schedule, class_name, course_name):
    schedule = ast.literal_eval(str(schedule))
    d = schedule[class_name][day]
    result = []
    for i in range(len(d)):
        if d[i] == course_name:
            result.append((d[i], i))
    return result


def check_for_conflixes(teacher_classes):
    res = 0
    for i in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
        res += get_day_conflixes(teacher_classes, i)
    return res


def get_day_conflixes(teacher_classes, day):
    days = []
    for c, d in teacher_classes.items():
        days.append((c, teacher_classes[c][day]))
    res = []
    for el in days:
        hours = el[1]
        for i in hours:
            res.append(i[1])
    if len(res) == len(set(res)):
        return 1  # no conflixes
    return 0  # a conflix appeared
