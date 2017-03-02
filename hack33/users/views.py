# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import (DetailView, ListView, RedirectView,
                                  UpdateView, TemplateView)
from django.views.generic.edit import FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User, SchoolSchedule
from .forms import EditProfileForm


class EditProfileView(FormView):
    template_name = 'edit_profile.html'
    form_class = EditProfileForm
    # success_url = '/thanks/'

    def get_success_url(self):
        return reverse('users:schedule-chart')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        import ipdb; ipdb.set_trace()
        return super(EditProfileView, self).form_valid(form)


class ScheduleChartView(TemplateView):
    template_name = 'schedule_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule'] = SchoolSchedule.objects.order_by('-rate')
        context['rate_lt_10'] = SchoolSchedule.objects.filter(rate__lt=0.1).all()
        context['rate_lt_20'] = SchoolSchedule.objects.filter(rate__gt=0.1, rate__lt=0.2)
        context['rate_lt_30'] = SchoolSchedule.objects.filter(rate__gt=0.2, rate__lt=0.3)
        context['rate_lt_40'] = SchoolSchedule.objects.filter(rate__gt=0.3, rate__lt=0.4)
        context['rate_lt_50'] = SchoolSchedule.objects.filter(rate__gt=0.4, rate__lt=0.5)
        context['rate_gt_50'] = SchoolSchedule.objects.filter(rate__gt=0.5)
        return context


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule'] = SchoolSchedule.objects.order_by('-rate').first()
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
