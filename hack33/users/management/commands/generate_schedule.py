from random import randint

from django.core.management.base import BaseCommand

from hack33.users.models import CourseClass, Students, SchoolSchedule

WEEK_DAYS = 5


class Command(BaseCommand):
    help = "Generate schedule per each class"

    def handle(self, **options):
        print("Start generating schedule ...\n")

        week_schedule = {}

        classes = Students.objects.all()
        for i in range(3000):
            print("Iteration")
            for c in classes:
                schedule = {
                    'monday': [],
                    'tuesday': [],
                    'wednesday': [],
                    'thursday': [],
                    'friday': []
                }
                course_classes = CourseClass.objects.filter(students=c).all()
                class_hours = sum([i.hours for i in course_classes])
                # hours_per_day = ceil(class_hours / WEEK_DAYS)
                course_hours = [[c.course.name, c.hours] for c in course_classes]
                print("Class: {}, Hours per week: {}".format(c.group_name, class_hours))
                for i in range(class_hours):
                    if len(course_hours) != 0:
                        random_day = list(schedule.keys())[randint(0, 4)]
                        random_number = randint(0, len(course_hours) - 1)
                        random_hour = course_hours[random_number]
                        random_hour[1] -= 1
                        schedule[random_day].append(random_hour[0])
                        if random_hour[1] == 0:
                            indx = course_hours.index(random_hour)
                            course_hours.pop(indx)
                # print(schedule)
                week_schedule[c.group_name] = schedule
            if not SchoolSchedule.objects.filter(schedule=week_schedule).exists():
                SchoolSchedule.objects.create(schedule=week_schedule)

            print("Population done")
