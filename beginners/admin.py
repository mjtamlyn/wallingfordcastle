import collections
import datetime
import functools

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminSplitDateTime
from django.db.models import Min
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils import timezone
from django.views.generic import FormView

from django_object_actions import (
    DjangoObjectActions, takes_instance_or_queryset,
)

from wallingford_castle.models import User

from .models import (
    STATUS_FAST_TRACK, STATUS_ON_COURSE, Beginner, BeginnersCourse,
    BeginnersCourseSession,
)


class BeginnersCourseSessionInline(admin.TabularInline):
    model = BeginnersCourseSession


class BeginnersCourseAddForm(forms.ModelForm):
    starts_at = forms.SplitDateTimeField(
        widget=AdminSplitDateTime,
        help_text='Defaults to four weekly 2 hour sessions. Can be changed later.',
    )

    class Meta:
        model = BeginnersCourse
        fields = []

    def save(self, **kwargs):
        self.instance.counter = 1
        most_recent_course = BeginnersCourse.objects.order_by('-counter').first()
        if most_recent_course:
            self.instance.counter = most_recent_course.counter + 1
        return super().save(**kwargs)

    def _save_m2m(self):
        """Override internals here to allow related objects to be created late."""
        for i in range(4):
            self.instance.beginnerscoursesession_set.create(
                start_time=self.cleaned_data['starts_at'] + datetime.timedelta(days=i * 7),
            )
        return self.instance


@admin.register(BeginnersCourse)
class BeginnersCourseAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'dates', 'number_on_course']
    add_form = BeginnersCourseAddForm

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        return [BeginnersCourseSessionInline]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.prefetch_related('beginner_set', 'beginnerscoursesession_set')

    def dates(self, instance):
        return ', '.join(
            str(session.start_time.strftime('%d %B %Y')) for session in instance.beginnerscoursesession_set.all()
        )

    def number_on_course(self, instance):
        return len(instance.beginner_set.all())


class BeginnersCourseChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '%s (starts %s)' % (obj, obj.start.strftime('%-d %B'))


class AllocateCourseForm(forms.Form):
    course = BeginnersCourseChoiceField(
        BeginnersCourse.objects.annotate(
            start=Min('beginnerscoursesession__start_time'),
        ).filter(
            start__gt=timezone.now() - datetime.timedelta(days=21),
        ),
        empty_label='Fast track',
        widget=forms.RadioSelect,
        required=False,
        blank=True,
    )


class AdminAllocateCourseView(FormView):
    template_name = 'admin/beginners/beginner/allocate.html'
    form_class = AllocateCourseForm

    def get_initial(self):
        return {'course': BeginnersCourse.objects.first()}

    def get_beginners(self):
        selected = self.request.GET['ids'].split(',')
        return Beginner.objects.filter(id__in=selected)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = Beginner._meta
        context['title'] = 'Allocate to course'
        context['beginners'] = self.get_beginners()
        return context

    def form_valid(self, form):
        beginners = self.get_beginners()
        course = form.cleaned_data['course']
        by_user = collections.defaultdict(list)
        for beginner in beginners:
            if course:
                beginner.course = course
                beginner.status = STATUS_ON_COURSE
            else:
                beginner.status = STATUS_FAST_TRACK
                beginner.fee = beginner.get_2020_fee()
            by_user[beginner.contact_email].append(beginner)
        for email, begs in by_user.items():
            user, created = User.objects.get_or_create(email=email, defaults={'is_active': False})
            for beginner in begs:
                beginner.user = user
                beginner.save()
            user.send_beginners_course_email(self.request, beginners=begs, course=course, created=created)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin:beginners_beginner_changelist')


@admin.register(Beginner)
class BeginnerAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['name', 'age', 'contact_email', 'course', 'status', 'fee', 'paid']
    list_filter = ['course', 'status']
    readonly_fields = ['created', 'modified']
    search_fields = ['name']
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
