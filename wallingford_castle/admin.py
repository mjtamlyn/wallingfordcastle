from django.contrib import admin

from .models import MembershipInterest, BeginnersCourseInterest


@admin.register(MembershipInterest)
class MembershipInterestAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'membership_type', 'status']
    list_filter = ['status', 'membership_type', 'age']
    actions = ['make_member']
    readonly_fields = ['created', 'modified']

    def make_member(self, request, queryset):
        for interest in queryset:
            interest.make_member(request)
    make_member.short_description = 'Promote to pending member'
    # TODO: make_member button on admin edit


@admin.register(BeginnersCourseInterest)
class BeginnersCourseInterestAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'modified']
