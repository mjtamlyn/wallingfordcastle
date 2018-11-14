from django.contrib import admin

from .models import Attendee, Booking, BookingQuestion, Event


class AttendeeInline(admin.TabularInline):
    model = Attendee
    autocomplete_fields = ['archer']


class BookingQuestionInline(admin.TabularInline):
    model = BookingQuestion


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end', 'attendee_count', 'bookable']
    list_filter = ['bookable']
    inlines = [AttendeeInline, BookingQuestionInline]
    ordering = ['-date']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['event', 'archer']
    list_filter = ['event']
    autocomplete_fields = ['archer']
