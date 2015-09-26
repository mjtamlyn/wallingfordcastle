from django.contrib import admin

from .models import Member


@admin.register(Member)
class MembershipInterestAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'membership_type', 'paid_until']
    list_filter = ['membership_type', 'age']
