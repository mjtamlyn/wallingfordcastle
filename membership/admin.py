from django.contrib import admin

from django_object_actions import DjangoObjectActions, takes_instance_or_queryset

from wallingford_castle.admin import ArcherDataMixin
from .models import Member


@admin.register(Member)
class MemberAdmin(DjangoObjectActions, ArcherDataMixin, admin.ModelAdmin):
    list_display = ['archer_name', 'archer_age', 'membership_type', 'active', 'archer_agb_number', 'archer_age_group', 'level']
    list_filter = ['active', 'membership_type', 'archer__age', 'level']
    readonly_fields = ['created', 'modified', 'archer_age', 'archer_agb_number', 'archer_date_of_birth', 'archer_age_group', 'archer_address', 'archer_contact_number']
    fields = [
        'archer',
        ('archer_agb_number', 'archer_age', 'archer_date_of_birth', 'archer_age_group'),
        ('archer_address', 'archer_contact_number'),
        'active',
        ('membership_type', 'level'),
        ('interest', 'created', 'modified'),
    ]
    actions = objectactions = ['update_plan']
    search_fields = ['archer__name']
    autocomplete_fields = ['archer']

    @takes_instance_or_queryset
    def update_plan(self, request, queryset):
        for member in queryset:
            member.archer.user.update_subscriptions()
    update_plan.short_description = 'Update plan'
    update_plan.label = 'Update plan'
