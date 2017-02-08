from django.core.management.base import BaseCommand

from hack33.users.models import Hour, CourseClass, Students, SchoolSchedule
from hack33.users.helpers.fitness import (is_any_empty_day, more_than_7_hours,
                                          give_rating_by_arrangement)
import json
import os
import ast
from math import ceil


WEEK_DAYS = 5

class Command(BaseCommand):
    help = "Fitness fucntion"

    def handle(self, **options):
        print("Fitness function on schedule population ...\n")
        f = 0
        all_schedules = SchoolSchedule.objects.all()
        print(all_schedules.count())
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
                # print(week_schedule)
                if is_any_empty_day(week_schedule):
                    SchoolSchedule.objects.filter(id=s.id).delete()
                    break
                if more_than_7_hours(week_schedule):
                    SchoolSchedule.objects.filter(id=s.id).delete()
                    break
            # give schedule rating
            # import ipdb; ipdb.set_trace()
            # if s.id == 2302:
                # print("innn")
            # if s.id == 2301:
            rating = give_rating_by_arrangement(schedule)
            if rating != 0:
                a = SchoolSchedule.objects.get(id=s.id)
                a.rate = rating/100
                a.save()
                f += 1
                print(f)
                print(rating)
                # print(week_schedule['monday'])
        # all_schedules = SchoolSchedule.objects.all()
        # print(all_schedules.count())
