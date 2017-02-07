from django.core.management.base import BaseCommand

from hack33.users.models import Hour, CourseClass, Students


class Command(BaseCommand):
    help = "Generate all hours per each class"

    def handle(self, **options):
        print("Start generating hours ...\n")

        students = Students.objects.all()
        for s in students:
            classes = CourseClass.objects.filter(students=s).all()
            for cl in classes:
                for i in range(cl.hours):
                    Hour.objects.create(course_class=cl)
                    print("Creating hour {} {}".format(s.group_name, cl.course))
