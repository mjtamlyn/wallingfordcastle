import copy
import datetime
import functools

from django import forms
from django.contrib import admin
from django.contrib.admin.helpers import AdminForm
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, FormView, ListView
from django.urls import path, reverse
from django.utils import html

from braces.views import MessageMixin
from dateutil.relativedelta import relativedelta
from django_object_actions import DjangoObjectActions, takes_instance_or_queryset

from events.models import Event
from wallingford_castle.admin import ArcherDataMixin
from wallingford_castle.models import Archer, User
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
        context['title'] = 'Summer signups summary'
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
            path('summary/', wrap(Summer2018Summary.as_view()), name='%s_%s_summary' % info),
        )
        return urls


@admin.register(CourseSignup)
class CourseSignupAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'email', 'student_date_of_birth', 'paid']


class SessionCreateEvent(MessageMixin, CreateView):
    template_name = 'admin/courses/session/create_event.html'
    model = Event
    fields = ['name', 'date', 'duration']

    def dispatch(self, request, *args, **kwargs):
        self.session = Session.objects.get(pk=self.kwargs['pk'])
        if self.session.event:
            self.messages.error('This session already has an event')
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        sessions = self.session.course.session_set.order_by('start_time')
        session_sequence = list(sessions).index(self.session) + 1
        return {
            'name': '%s - session #%s' % (self.session.course, session_sequence),
            'date': self.session.start_time,
            'duration': self.session.duration,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create event for %s on %s' % (self.session.course, self.session.start_time.date())
        context['opts'] = Session._meta
        context['add'] = True
        context['change'] = False
        context['is_popup'] = False
        context['save_as'] = False
        context['has_add_permission'] = self.request.user.has_perm('events.add_event')
        context['has_change_permission'] = self.request.user.has_perm('events.change_event')
        context['has_view_permission'] = self.request.user.has_perm('events.view_event')
        context['has_delete_permission'] = self.request.user.has_perm('events.delete_event')
        context['has_editable_inline_admin_formsets'] = False
        context['adminform'] = AdminForm(context['form'], fieldsets=[(None, {'fields': self.fields})], prepopulated_fields={})
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.session.event = form.instance
        self.session.save(update_fields=['event_id'])
        return response

    def get_success_url(self):
        return reverse('admin:courses_course_sessions', kwargs={'course_id': self.session.course_id})


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return functools.update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urls = [
            path('<pk>/create-event/', wrap(SessionCreateEvent.as_view()), name='%s_%s_create_event' % info),
        ] + urls
        return urls



class SessionInline(admin.TabularInline):
    model = Session
    readonly_fields = ['event']


class CourseReport(DetailView):
    model = Course
    template_name = 'admin/courses/course/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = Course._meta
        context['title'] = 'Report for %s' % self.object
        context['attendees'] = self.object.attendee_set.order_by('created').select_related('archer', 'archer__user')
        context['has_groups'] = self.object.attendee_set.exclude(group='').exists()
        if context['has_groups']:
            groups = self.object.attendee_set.exclude(group='').values('group').annotate(attendee_count=Count('id'))
            context['groups'] = sorted(groups, key=lambda g: g['group'])
        return context


class CourseSessions(ListView):
    model = Session
    template_name = 'admin/courses/course/sessions.html'

    def get_queryset(self):
        self.object = Course.objects.get(pk=self.kwargs['course_id'])
        return Session.objects.filter(course=self.object).order_by('start_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = Course._meta
        context['session_opts'] = Session._meta
        context['title'] = 'Sessions for %s' % self.object
        context['object'] = self.object
        return context


@admin.register(Course)
class CourseAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['name', 'course_start_date', 'report_link']
    readonly_fields = ['created', 'modified']
    inlines = [SessionInline]
    change_actions = ['view_report']

    def get_urls(self):
        urls = super().get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return functools.update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urls = [
            path('<pk>/report/', wrap(CourseReport.as_view()), name='%s_%s_report' % info),
            path('<course_id>/sessions/', wrap(CourseSessions.as_view()), name='%s_%s_sessions' % info),
        ] + urls
        return urls

    def course_start_date(self, obj):
        first_session = obj.session_set.order_by('start_time').first()
        if first_session:
            return first_session.start_time.date()
        return 'No sessions'

    def report_link(self, obj):
        return html.format_html('''
            <a href="{}" title="View report">
                View report >
            </a>
        ''', reverse('admin:%s_%s_report' % (self.model._meta.app_label, self.model._meta.model_name), kwargs={'pk': obj.pk}))
    report_link.short_description = 'View report'

    def view_report(self, request, instance):
        url = reverse('admin:%s_%s_report' % (self.model._meta.app_label, self.model._meta.model_name), kwargs={'pk': instance.pk})
        return HttpResponseRedirect(url)
    view_report.short_description = 'View report'
    view_report.label = 'View report'


@admin.register(Attendee)
class AttendeeAdmin(ArcherDataMixin, admin.ModelAdmin):
    list_display = ['archer', 'course', 'group', 'paid', 'member']
    list_filter = ['course', 'paid', 'member']
    readonly_fields = ['created', 'modified', 'archer_age', 'archer_agb_number', 'archer_date_of_birth', 'archer_age_group', 'archer_address', 'archer_contact_number', 'archer_email']
    fields = [
        ('archer', 'course'),
        'group',
        'member',
        ('archer_agb_number', 'archer_age', 'archer_date_of_birth', 'archer_age_group'),
        ('archer_address', 'archer_contact_number', 'archer_email'),
        'contact_name',
        ('experience', 'notes', 'communication_notes'),
        ('gdpr_consent', 'contact'),
        'paid',
        ('created', 'modified'),
    ]


class AllocateCourseForm(forms.Form):
    course = forms.ModelChoiceField(
        Course.objects,
        widget=forms.RadioSelect,
    )

    def __init__(self, interests, request, **kwargs):
        self.request = request
        self.interests = interests
        super().__init__(**kwargs)

    def clean(self):
        for interest in self.interests:
            if interest.processed:
                self.add_error(None, forms.ValidationError('%(interest)s is already processed', params={'interest': interest}))

    def save(self):
        new_users = set()
        existing_users = set()
        for interest in self.interests:
            user, created = User.objects.get_or_create(
                email=interest.contact_email,
                defaults={
                    'is_active': False,
                }
            )
            if created:
                new_users.add(user)
            else:
                existing_users.add(user)
            today = datetime.date.today()
            age = relativedelta(today, interest.date_of_birth).years
            archer, _ = Archer.objects.get_or_create(
                name=interest.name,
                user=user,
                defaults={
                    'date_of_birth': interest.date_of_birth,
                    'age': 'senior' if age >= 18 else 'junior',
                    'contact_number': interest.contact_number,
                }
            )
            if archer.member_set.exists():
                self.add_error(None, forms.ValidationError('%(name)s is already a member', params={'name': archer}))
                raise ValueError('Tried to allocate a member to a non-member course')
            Attendee.objects.create(
                course=self.cleaned_data['course'],
                archer=archer,
                experience=interest.experience,
                notes=interest.notes,
                gdpr_consent=interest.gdpr_consent,
                contact=interest.contact,
                member=False,
            )
            interest.processed = True
            interest.save()
        for user in new_users:
            user.send_course_email(request=self.request, new_user=True)
        for user in existing_users:
            user.send_course_email(request=self.request, new_user=False)


class AdminAllocateCourseView(FormView):
    template_name = 'admin/courses/interest/allocate.html'
    form_class = AllocateCourseForm

    def get_interests(self):
        selected = self.request.GET['ids'].split(',')
        return Interest.objects.filter(id__in=selected)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = Interest._meta
        context['title'] = 'Allocate to course'
        context['interests'] = self.get_interests()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['interests'] = self.get_interests()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        try:
            with transaction.atomic():
                form.save()
        except ValueError:
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin:courses_interest_changelist')


@admin.register(Interest)
class InterestAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['name', 'course_type', 'contact_email', 'date_of_birth', 'processed']
    list_filter = ['processed', 'course_type']
    actions = change_actions = ['allocate_to_course']

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
            path('allocate/', wrap(AdminAllocateCourseView.as_view()), name='%s_%s_allocate' % info),
        )
        return urls

    @takes_instance_or_queryset
    def allocate_to_course(self, request, queryset):
        url = reverse('admin:%s_%s_allocate' % (self.model._meta.app_label, self.model._meta.model_name))
        return HttpResponseRedirect(url + '?ids=%s' % ','.join(str(item.pk) for item in queryset))
    allocate_to_course.short_description = 'Allocate to a course'
    allocate_to_course.label = 'Allocate to a course'
