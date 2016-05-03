from django.contrib import admin

from django_object_actions import DjangoObjectActions, takes_instance_or_queryset

from .models import Member


@admin.register(Member)
class MemberAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['name', 'age', 'membership_type', 'active', 'squad', 'agb_number']
    list_filter = ['active', 'membership_type', 'age', 'squad']
    readonly_fields = ['created', 'modified']
    actions = objectactions = ['update_plan']

    @takes_instance_or_queryset
    def update_plan(self, request, queryset):
        for member in queryset:
            member.update_plan()
    update_plan.short_description = 'Update plan'
    update_plan.label = 'Update plan'
