from django.contrib import admin

from custom_user.admin import EmailUserAdmin
from django_object_actions import DjangoObjectActions, takes_instance_or_queryset

from .models import MembershipInterest, BeginnersCourseInterest, User


@admin.register(MembershipInterest)
class MembershipInterestAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['name', 'age', 'membership_type', 'status']
    list_filter = ['status', 'membership_type', 'age']
    actions = objectactions = ['make_member', 'send_to_beginners']
    readonly_fields = ['created', 'modified']

    @takes_instance_or_queryset
    def make_member(self, request, queryset):
        for interest in queryset:
            interest.make_member(request)
    make_member.short_description = 'Promote to pending member'
    make_member.label = 'Make pending member'

    @takes_instance_or_queryset
    def send_to_beginners(self, request, queryset):
        for interest in queryset:
            interest.send_to_beginners()
    send_to_beginners.short_description = 'Send to beginners course'
    send_to_beginners.label = 'Send to beginners course'


@admin.register(BeginnersCourseInterest)
class BeginnersCourseInterestAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'contact_email']
    readonly_fields = ['created', 'modified']


@admin.register(User)
class UserAdmin(DjangoObjectActions, EmailUserAdmin):
    actions = objectactions = ['send_welcome_email']

    @takes_instance_or_queryset
    def send_welcome_email(self, request, queryset):
        for user in queryset:
            user.send_welcome_email(request)
    send_welcome_email.short_description = 'Send welcome email'
    send_welcome_email.label = 'Send welcome email'
