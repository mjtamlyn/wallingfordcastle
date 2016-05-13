import collections
import functools

from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from django_object_actions import DjangoObjectActions, takes_instance_or_queryset

from wallingford_castle.models import User

from .models import STATUS_ON_COURSE, Beginner, BeginnersCourse, BeginnersCourseSession


class BeginnersCourseSessionInline(admin.TabularInline):
    model = BeginnersCourseSession


@admin.register(BeginnersCourse)
class BeginnersCourseAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'dates', 'number_on_course']
    inlines = [BeginnersCourseSessionInline]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.prefetch_related('beginner_set', 'beginnerscoursesession_set')

    def dates(self, instance):
        return ', '.join(
            str(session.start_time.strftime('%d %B %Y')) for session in instance.beginnerscoursesession_set.all()
        )

    def number_on_course(self, instance):
        return len(instance.beginner_set.all())


class AllocateCourseForm(forms.Form):
    course = forms.ModelChoiceField(
        BeginnersCourse.objects,
        empty_label=None,
        widget=forms.RadioSelect,
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
        context['beginners'] = self.get_beginners()
        return context

    def form_valid(self, form):
        beginners = self.get_beginners()
        course = form.cleaned_data['course']
        by_user = collections.defaultdict(list)
        for beginner in beginners:
            beginner.course = course
            beginner.status = STATUS_ON_COURSE
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
    list_display = ['name', 'age', 'contact_email', 'course', 'status', 'paid']
    list_filter = ['course', 'status']
    readonly_fields = ['created', 'modified']
    actions = objectactions = ['allocate_to_course']

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
            url(r'^allocate/$', wrap(AdminAllocateCourseView.as_view()), name='%s_%s_allocate' % info),
        )
        return urls

    @takes_instance_or_queryset
    def allocate_to_course(self, request, queryset):
        url = reverse('admin:%s_%s_allocate' % (self.model._meta.app_label, self.model._meta.model_name))
        return HttpResponseRedirect(url + '?ids=%s' % ','.join(str(item.pk) for item in queryset))
    allocate_to_course.short_description = 'Allocate to a course'
    allocate_to_course.label = 'Allocate to a course'
