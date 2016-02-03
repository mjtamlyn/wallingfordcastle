from django.contrib import admin

from .models import Beginner


@admin.register(Beginner)
class BeginnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'contact_email', 'course', 'status']
    list_filter = ['course', 'status']
    readonly_fields = ['created', 'modified']
