from django.contrib import admin

from .models import Attendee, Event


class AttendeeInline(admin.TabularInline):
    model = Attendee
    autocomplete_fields = ['member']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end', 'attendee_count']
    inlines = [AttendeeInline]
    ordering = ['date']
