from django.db import models


class CourseClassQuerySet(models.QuerySet):

    def get_teacher_classes(self, teacher):
        return self.filter(teacher__id=teacher.id).all()
