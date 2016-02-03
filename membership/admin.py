from django.contrib import admin

from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'membership_type', 'has_payment_setup', 'agb_number']
    list_filter = ['membership_type', 'age']
    readonly_fields = ['created', 'modified']

    def has_payment_setup(self, instance):
        return bool(instance.subscription_id)
    has_payment_setup.boolean = True
