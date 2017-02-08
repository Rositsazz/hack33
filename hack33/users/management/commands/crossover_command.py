import ast
from random import randint
from math import ceil

from django.core.management.base import BaseCommand

from hack33.users.models import SchoolSchedule

WEEK_DAYS = 5
TEACHER_CLASSES_POINTS = 1


class Command(BaseCommand):
    help = "Crossover function"

    def handle(self, **options):
        print("""Crossover starts...\n
From each parent get 2 week schedules\n""")

        schedules = SchoolSchedule.objects.order_by("-rate")
        population = schedules[:100:]
        for i in range(len(population) - 1):
            parent1 = population[i]
            parent_1_classes = list(parent1.schedule.keys())
            # print(parent_1_classes)
            child_schedule = {}
            for j in range(ceil(len(parent_1_classes) / 2)):
                random_number = randint(0, len(parent_1_classes) - 1)
                # print(random_number)
                class_name = parent_1_classes[random_number]
                # print(class_name)
                child_schedule[class_name] = parent1.schedule[class_name]
            # print(child_schedule)
            parent2 = population[i + 1]
            parent_2_classes = list(parent1.schedule.keys())
            for j in range(len(parent_2_classes)):
                current_class = parent_2_classes[j]
                if not current_class in child_schedule:
                    class_name = current_class
                    child_schedule[class_name] = parent2.schedule[class_name]
            print("Creating child...")
            SchoolSchedule.objects.create(schedule=child_schedule)
            # print(child_schedule)
        all_schedules = SchoolSchedule.objects.all()
        print("Current population: {}".format(all_schedules.count()))
