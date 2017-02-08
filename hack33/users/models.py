# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from jsonfield import JSONField


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class Teacher(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Students(models.Model):
    group_name = models.CharField(max_length=255)
    number = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.group_name


class Classroom(models.Model):
    CLASS_ROOM = 0
    SPORT = 1
    READING = 2
    COMPUTER = 3
    LABORATORY = 4

    ROOM_CHOICE = (
        (CLASS_ROOM, 'class_room'),
        (SPORT, 'sport'),
        (READING, 'reading'),
        (COMPUTER, 'computer'),
        (LABORATORY, 'laboratory'),
    )

    name = models.CharField(max_length=255)
    number_of_seats = models.IntegerField(default=0, blank=False, null=False)
    room_type = models.SmallIntegerField(choices=ROOM_CHOICE, default=CLASS_ROOM)


class Course(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CourseClass(models.Model):
    CLASS_ROOM = 0
    SPORT = 1
    READING = 2
    COMPUTER = 3
    LABORATORY = 4

    ROOM_CHOICE = (
        (CLASS_ROOM, 'class_room'),
        (SPORT, 'sport'),
        (READING, 'reading'),
        (COMPUTER, 'computer'),
        (LABORATORY, 'laboratory'),
    )
    course = models.ForeignKey(Course)
    teacher = models.ForeignKey(Teacher)
    students = models.ForeignKey(Students)
    course_type = models.SmallIntegerField(choices=ROOM_CHOICE, default=CLASS_ROOM)
    hours = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return "{} - {}".format(self.course.name, self.students.group_name)


class Hour(models.Model):
    room = models.ForeignKey(Classroom, blank=True, null=True)
    course_class = models.ForeignKey(CourseClass)

    def __str__(self):
        return "{}".format(self.course_class)


class SchoolSchedule(models.Model):
    schedule = JSONField()
    rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], default=0)
