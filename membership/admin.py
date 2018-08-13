from django.contrib import admin

from django_object_actions import DjangoObjectActions, takes_instance_or_queryset

from .models import Member


@admin.register(Member)
class MemberAdmin(DjangoObjectActions, admin.ModelAdmin):
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

    def archer_name(self, obj):
        return obj.archer.name
    archer_name.short_description = 'Name'

    def archer_age(self, obj):
        return obj.archer.get_age_display()
    archer_age.short_description = 'Age'

    def archer_agb_number(self, obj):
        return obj.archer.agb_number
    archer_agb_number.short_description = 'AGB number'

    def archer_date_of_birth(self, obj):
        return obj.archer.date_of_birth
    archer_date_of_birth.short_description = 'DOB'

    def archer_age_group(self, obj):
        return obj.archer.age_group
    archer_age_group.short_description = 'Age group'
    archer_age_group.admin_order_field = 'archer__date_of_birth'

    def archer_address(self, obj):
        return obj.archer.address
    archer_address.short_description = 'Address'

    def archer_contact_number(self, obj):
        return obj.archer.contact_number
    archer_contact_number.short_description = 'Contact number'

    @takes_instance_or_queryset
    def update_plan(self, request, queryset):
        for member in queryset:
            member.update_plan()
    update_plan.short_description = 'Update plan'
    update_plan.label = 'Update plan'

