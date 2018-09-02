import copy
import datetime
import functools

from django.conf.urls import url
from django.contrib import admin
from django.views.generic import ListView

from wallingford_castle.admin import ArcherDataMixin
from .models import Attendee, Course, CourseSignup, Interest, Session, Summer2018Signup


class Summer2018Summary(ListView):
    model = Summer2018Signup
    template_name = 'admin/courses/summer2018_signup/summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sessions = (
            ('6-12 beginners', []),
            ('6-12 intermediates', []),
            ('12-18 beginners', []),
            ('12-18 intermediates', []),
        )
        dates = (
            (datetime.date(2018, 7, 26), copy.deepcopy(sessions)),
            (datetime.date(2018, 7, 31), copy.deepcopy(sessions)),
            (datetime.date(2018, 8, 2), copy.deepcopy(sessions)),
            (datetime.date(2018, 8, 7), copy.deepcopy(sessions)),
            (datetime.date(2018, 8, 9), copy.deepcopy(sessions)),
            (datetime.date(2018, 8, 14), copy.deepcopy(sessions)),
            (datetime.date(2018, 8, 16), copy.deepcopy(sessions)),
            (datetime.date(2018, 8, 21), copy.deepcopy(sessions)),
            (datetime.date(2018, 8, 23), copy.deepcopy(sessions)),
            (datetime.date(2018, 8, 28), copy.deepcopy(sessions)),
            (datetime.date(2018, 8, 30), copy.deepcopy(sessions)),
            (datetime.date(2018, 9, 4), copy.deepcopy(sessions)),
        )
        for archer in context['object_list']:
            for date, date_sessions in dates:
                if date in archer.dates:
                    for session, names in date_sessions:
                        if session == archer.group:
                            names.append(archer.student_name)

        context['summary'] = dates
        context['opts'] = Summer2018Signup._meta
        return context


@admin.register(Summer2018Signup)
class Summer2018SignupAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'email', 'student_date_of_birth', 'dates', 'group', 'paid']
    list_filter = ['group']

    def get_urls(self):
        urls = super().get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return functools.update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urls.insert(
            0,
            url(r'^summary/$', wrap(Summer2018Summary.as_view()), name='%s_%s_summary' % info),
        )
        return urls


@admin.register(CourseSignup)
class CourseSignupAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'email', 'student_date_of_birth', 'paid']


class SessionInline(admin.TabularInline):
    model = Session


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_start_date']
    readonly_fields = ['created', 'modified']
    inlines = [SessionInline]

    def course_start_date(self, obj):
        first_session = obj.session_set.order_by('start_time').first()
        if first_session:
            return first_session.start_time.date()
        return 'No sessions'


@admin.register(Attendee)
class AttendeeAdmin(ArcherDataMixin, admin.ModelAdmin):
    list_display = ['archer', 'course', 'paid', 'member']
    list_filter = ['course', 'paid', 'member']
    readonly_fields = ['created', 'modified', 'archer_age', 'archer_agb_number', 'archer_date_of_birth', 'archer_age_group', 'archer_address', 'archer_contact_number']
    fields = [
        ('archer', 'course'),
        'member',
        ('archer_agb_number', 'archer_age', 'archer_date_of_birth', 'archer_age_group'),
        ('archer_address', 'archer_contact_number'),
        'contact_name',
        ('experience', 'notes', 'communication_notes'),
        ('gdpr_consent', 'contact'),
        'paid',
        ('created', 'modified'),
    ]


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_type', 'contact_email', 'date_of_birth', 'processed']
    list_filter = ['processed', 'course_type']
