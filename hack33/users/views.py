# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import (DetailView, ListView, RedirectView,
                                  UpdateView, TemplateView)

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User
from math import ceil


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # courses = Course.objects.all()
        # school_class = SchoolClass.objects.first()
        # class_courses = school_class.courses.order_by('-hours')
        # course_hours = [[c.name, c.hours] for c in class_courses]
        # hours = sum([course.hours for course in class_courses])
        # hours_per_day = ceil(hours / 5)
        # days2 = {
        #     'monday': [],
        #     'tuesday': [],
        #     'wedn': [],
        #     'thur': [],
        #     'friday': []
        # }
        # course_hours2 = [[c.name, c.hours] for c in class_courses]
        # max_h = course_hours2[0][1]
        # diff = ceil(max_h / hours_per_day)
        # for i in range(diff):
        #     for k, v in days2.items():
        #         for i in range(hours_per_day):
        #             c, h = course_hours2[i]
        #             if h > 0:
        #                 v.append(c)
        #                 course_hours2[i][1] -= 1
        # with open('examples.txt', 'r+') as f:
        #     f.write(str(days2))
        #     f.write("\n" + "="*80)
        # # import ipdb; ipdb.set_trace()
        # context['days'] = days2
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
