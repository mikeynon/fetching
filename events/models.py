# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import Field
from django.urls import reverse
from django.db import models
from django import forms
from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe
from itertools import groupby
from calendar import HTMLCalendar, monthrange
from django.contrib.admin import widgets
import datetime

class ContestCalendar(HTMLCalendar):

    def __init__(self, pContestEvents):
        super(ContestCalendar, self).__init__()
        self.contest_events = self.group_by_day(pContestEvents)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.contest_events:
                cssclass += ' filled'
                body = []
                for contest in self.contest_events[day]:
                    body.append('<a href="%s">' % contest.get_absolute_url())
                    body.append(esc(contest.contest.name))
                    body.append('</a><br/>')
                return self.day_cell(cssclass, '<div class="dayNumber">%d</div> %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, '<div class="dayNumber">%d</div>' % day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(ContestCalendar, self).formatmonth(year, month)

    def group_by_day(self, pContestEvents):
        field = lambda contest: contest.date_of_event.day
        return dict(
            [(day, list(items)) for day, items in groupby(pContestEvents, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


class Event(models.Model):
    # day = models.DateField(u'Day of the event', help_text=u'Start Date')
    # subject = models.TextField(u'Band Name', help_text=u'Band Name', blank=True, null=True)
    day = models.DateField(help_text=u'Start Date')
    # day = models.DateField(u'End Date', help_text=u'End Date')
    start_time = models.TimeField(help_text=u'Starting time')
    end_time = models.TimeField(help_text=u'Ending time')
    # all_day_event = models.BooleanField(initial=False)
    notes = models.TextField(blank=True, null=True)
    # private = models.BooleanField(initial=False)
    likes = models.IntegerField(default=0)
    space = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Scheduling'
        verbose_name_plural = 'Scheduling'

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:  # edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (
                new_end >= fixed_start and new_end <= fixed_end):  # innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
            overlap = True

        return overlap

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s at %s</a>' % (url, str(self.notes), str(self.start_time))

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Cant End before it Starts!')

        events = Event.objects.filter(day=self.day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        'There is an overlap with another event: ' + str(event.day) + ', ' + str(
                            event.start_time) + '-' + str(event.end_time))

    class IPAddressField(Field):
        system_check_deprecated_details = {
            'msg': (
                'IPAddressField has been deprecated. Support for it (except '
                'in historical migrations) will be removed in Django 1.9.'
            ),
            'hint': 'Use GenericIPAddressField instead.',  # optional
            'id': 'fields.W900',  # pick a unique ID for your field.
        }

class band(models.Model):
    name = models.CharField(blank=True, null=True,max_length= 100)
    website = models.CharField(blank=True, null=True,max_length= 200)
    social_media = models.CharField(blank=True, null=True,max_length= 100)
    bandpic = models.FileField(upload_to = 'static/images')
    def __str__(self):
        return self.name + ', '+ self.website + ', ' + self.social_media

class venueLocation(models.Model):
    street = models.CharField(blank=True, null=True, max_length= 100)
    city = models.CharField(blank=True, null=True, max_length= 100)
    state = models.CharField(blank=True, null=True, max_length= 100)

    def __str__(self):
        return self.street + ' ' + self.city + ', ' + self.state

class venue(models.Model):
    name = models.CharField(blank=True, null=True, max_length= 100)
    website = models.CharField(blank=True, null=True, max_length= 200)
    social_media = models.CharField(help_text='include @', blank=True, null=True, max_length= 100)
    location = models.ForeignKey(venueLocation, on_delete=models.CASCADE)
    # secret = models.BooleanField(initial=False)

    def __str__(self):
        return self.name

class searchBandSugg(models.Model):
    name = models.CharField(blank=True, null=True, max_length=100)
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)

    def __str__(self):
        return self.name +" added."

    def get_absolute_url(self):
        return reverse('shows')

class Document(models.Model):
    # date = forms.DateField(required=False)
    document = models.ImageField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # band = models.CharField(max_length=255, blank=True)
    # venue = models.CharField(max_length=255, blank=True)

