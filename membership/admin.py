import functools

from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.views.generic import FormView

from django_object_actions import (
    DjangoObjectActions, takes_instance_or_queryset,
)

from courses.models import Attendee, Course
from wallingford_castle.admin import ArcherDataMixin

from .models import Member


class AdminBookCourseForm(forms.Form):
    course = forms.ModelChoiceField(
        Course.objects,
        widget=forms.RadioSelect,
        required=True,
    )

    def __init__(self, members, **kwargs):
        self.members = members
        super().__init__(**kwargs)

    def save(self):
        course = self.cleaned_data['course']
        for member in self.members:
            member.archer.user.add_invoice_item(
                amount=course.members_price * 100,
                description='%s for %s' % (course, member),
            )
            Attendee.objects.create(
                course=course,
                archer=member.archer,
                paid=True,
            )


class AdminBookCourseView(FormView):
    template_name = 'admin/membership/member/book_course.html'
    form_class = AdminBookCourseForm

    def get_form_kwargs(self):
        selected = self.request.GET['ids'].split(',')
        self.members = Member.objects.filter(id__in=selected)
        kwargs = super().get_form_kwargs()
        kwargs['members'] = self.members
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = Member._meta
        context['members'] = self.members
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin:membership_member_changelist')


@admin.register(Member)
class MemberAdmin(DjangoObjectActions, ArcherDataMixin, admin.ModelAdmin):
    list_display = [
        'archer_name', 'archer_age', 'membership_type',
        'coaching_subscription', 'active', 'archer_agb_number',
        'archer_age_group',
    ]
    list_filter = ['active', 'membership_type', 'coaching_subscription', 'archer__age']
    readonly_fields = [
        'created', 'modified', 'archer_age', 'archer_agb_number',
        'archer_date_of_birth', 'archer_age_group', 'archer_address',
        'archer_contact_number', 'archer_email',
    ]
    fields = [
        'archer',
        ('archer_agb_number', 'archer_age', 'archer_date_of_birth', 'archer_age_group'),
        ('archer_address', 'archer_contact_number', 'archer_email'),
        'active',
        ('membership_type', 'coaching_subscription', 'level'),
        ('interest', 'created', 'modified'),
    ]
    actions = change_actions = ['update_plan', 'book_into_course']
    search_fields = ['archer__name']
    autocomplete_fields = ['archer']

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
            path('book_course/', wrap(AdminBookCourseView.as_view()), name='%s_%s_book_course' % info),
        )
        return urls

    @takes_instance_or_queryset
    def update_plan(self, request, queryset):
        for member in queryset:
            member.archer.user.update_subscriptions()
    update_plan.short_description = 'Update plan'
    update_plan.label = 'Update plan'

    @takes_instance_or_queryset
    def book_into_course(self, request, queryset):
        url = reverse('admin:%s_%s_book_course' % (self.model._meta.app_label, self.model._meta.model_name))
        return HttpResponseRedirect(url + '?ids=%s' % ','.join(str(item.pk) for item in queryset))
    book_into_course.short_description = 'Book into course'
    book_into_course.label = 'Book into course'
