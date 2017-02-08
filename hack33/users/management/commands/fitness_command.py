from django.core.management.base import BaseCommand

from hack33.users.models import (Hour, CourseClass, Students, SchoolSchedule,
                                 Teacher)
from hack33.users.helpers.fitness import (is_any_empty_day,
                                          more_than_7_hours,
                                          give_rating_by_arrangement,
                                          less_than_2_hours,
                                          check_teachers_schedule,
                                          get_course_indxes_by_day,
                                          check_for_conflixes,
                                          get_day_conflixes)
import json
import os
import ast
from math import ceil


WEEK_DAYS = 5
TEACHER_CLASSES_POINTS = 1


class Command(BaseCommand):
    help = "Fitness fucntion"

    def handle(self, **options):
        print("Fitness function on schedule population ...\n")
        all_schedules = SchoolSchedule.objects.all()
        print(all_schedules.count())

        # remove invalid schedules
        for s in all_schedules:
            schedule = ast.literal_eval(str(s))
            for c, week_schedule in schedule.items():
                students = Students.objects.get(group_name=c)
                course_hours = list(Hour.objects.filter(course_class__students=students).all())
                class_hours = len(course_hours)
                monday = week_schedule['monday']
                tuesday = week_schedule['tuesday']
                wednesday = week_schedule['wednesday']
                thursday = week_schedule['thursday']
                friday = week_schedule['friday']
                hours_per_day = ceil(class_hours / WEEK_DAYS)

                if is_any_empty_day(week_schedule):
                    SchoolSchedule.objects.filter(id=s.id).delete()
                    break

                if more_than_7_hours(week_schedule):
                    SchoolSchedule.objects.filter(id=s.id).delete()
                    break

                if less_than_2_hours(week_schedule):
                    SchoolSchedule.objects.filter(id=s.id).delete()
                    break

        # get rating
        all_schedules = SchoolSchedule.objects.all()
        for s in all_schedules:
            schedule = ast.literal_eval(str(s))
            # rating by arrangement
            rating = give_rating_by_arrangement(schedule)
            if rating != 0:
                a = SchoolSchedule.objects.get(id=s.id)
                a.rate = rating/100
                a.save()

            # rating by teacher conflixes
            rating_by_teacher_conflixes = check_teachers_schedule(s)
            f = SchoolSchedule.objects.get(id=s.id)
            f.rate += rating_by_teacher_conflixes/100
            f.save()
        all_schedules = SchoolSchedule.objects.all()
        print(all_schedules.count())
