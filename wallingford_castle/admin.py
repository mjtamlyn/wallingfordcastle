from django.contrib import admin

from custom_user.admin import EmailUserAdmin
from django_object_actions import DjangoObjectActions, takes_instance_or_queryset

from .models import Archer, MembershipInterest, User


@admin.register(Archer)
class ArcherAdmin(admin.ModelAdmin):
    list_display = ['name', 'agb_number', 'date_of_birth', 'age_group']
    search_fields = ['name']
    autocomplete_fields = ['user', 'managing_users']


class ArcherDataMixin(object):
    """Utility mixin class for ModelAdmins which reference archer data."""

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


@admin.register(MembershipInterest)
class MembershipInterestAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['name', 'age', 'membership_type', 'status']
    list_filter = ['status', 'membership_type', 'age']
    actions = change_actions = ['make_member', 'send_to_beginners']
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


@admin.register(User)
class UserAdmin(DjangoObjectActions, EmailUserAdmin):
    actions = change_actions = ['send_new_user_email', 'send_welcome_email']
    fieldsets = EmailUserAdmin.fieldsets + (
        ('Internal fields', {
            'fields': ('customer_id', 'tournament_only', 'generate_register_url')
        }),
    )
    readonly_fields = ['generate_register_url']

    def generate_register_url(self, instance):
        return instance.generate_register_url()

    @takes_instance_or_queryset
    def send_new_user_email(self, request, queryset):
        for user in queryset:
            user.send_new_user_email(request)
    send_new_user_email.short_description = 'Send new user email'
    send_new_user_email.label = 'Send new user email'

    @takes_instance_or_queryset
    def send_welcome_email(self, request, queryset):
        for user in queryset:
            user.send_welcome_email(request)
    send_welcome_email.short_description = 'Send welcome email'
    send_welcome_email.label = 'Send welcome email'
