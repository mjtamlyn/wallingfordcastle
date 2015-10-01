from django.contrib import admin

from custom_user.admin import EmailUserAdmin
from django_object_actions import DjangoObjectActions, takes_instance_or_queryset

from .models import MembershipInterest, BeginnersCourseInterest, User


@admin.register(MembershipInterest)
class MembershipInterestAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['name', 'age', 'membership_type', 'status']
    list_filter = ['status', 'membership_type', 'age']
    actions = objectactions = ['make_member']
    readonly_fields = ['created', 'modified']

    @takes_instance_or_queryset
    def make_member(self, request, queryset):
        for interest in queryset:
            interest.make_member(request)
    make_member.short_description = 'Promote to pending member'
    make_member.label = 'Make pending member'


@admin.register(BeginnersCourseInterest)
class BeginnersCourseInterestAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'modified']


@admin.register(User)
class UserAdmin(EmailUserAdmin):
    pass
