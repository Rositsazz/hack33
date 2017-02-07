from django.core.management.base import BaseCommand

from hack33.users.models import Hour, CourseClass, Students, SchoolSchedule
import json
import os

WEEK_DAYS = 5

class Command(BaseCommand):
    help = "Fitness fucntion"

    def handle(self, **options):
        print("Fitness function on schedule population ...\n")
