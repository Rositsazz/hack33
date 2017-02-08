import ast

from django.core.management.base import BaseCommand

from hack33.users.models import SchoolSchedule
from hack33.users.helpers.fitness import (is_any_empty_day,
                                          more_than_7_hours,
                                          give_rating_by_arrangement,
                                          less_than_2_hours,
                                          check_teachers_schedule)

WEEK_DAYS = 5
TEACHER_CLASSES_POINTS = 1


class Command(BaseCommand):
    help = "Fitness function"

    def handle(self, **options):
        print("Fitness function on schedule population ...\n")
        all_schedules = SchoolSchedule.objects.all()
        print(all_schedules.count())

        # remove invalid schedules
        for s in all_schedules:
            schedule = ast.literal_eval(str(s))
            for c, week_schedule in schedule.items():
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
            s.rate = 0
            # rating by arrangement
            rating = give_rating_by_arrangement(schedule)
            if rating != 0:
                # a = SchoolSchedule.objects.get(id=s.id)
                # a.rate = rating/100
                s.rate = rating / 100
                s.save()

            # rating by teacher conflixes
            rating_by_teacher_conflixes = check_teachers_schedule(s)
            # f = SchoolSchedule.objects.get(id=s.id)
            s.rate += rating_by_teacher_conflixes/100
            s.save()
        all_schedules = SchoolSchedule.objects.all()
        print(all_schedules.count())
