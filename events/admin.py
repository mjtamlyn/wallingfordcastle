import functools

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.views.generic import DetailView

from django_object_actions import (
    DjangoObjectActions, takes_instance_or_queryset,
)

from .models import (
    Attendee, BookedSlot, Booking, BookingQuestion, BookingTemplate, Event,
)


class AttendeeInline(admin.TabularInline):
    model = Attendee
    autocomplete_fields = ['archer']

    def get_extra(self, request, obj=None, **kwargs):
        if obj is None:
            return 20
        return 3


class BookingQuestionInline(admin.TabularInline):
    model = BookingQuestion


class BookingReport(DetailView):
    model = Event
    template_name = 'admin/events/event/booking_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = Event._meta
        if self.object.bookable:
            context['bookings'] = self.object.booking_set.order_by('id')
            context['questions'] = self.object.bookingquestion_set.order_by('order')
        return context


@admin.register(Event)
class EventAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['name', 'start', 'end', 'attendee_count', 'bookable']
    list_filter = ['bookable']
    inlines = [AttendeeInline, BookingQuestionInline]
    ordering = ['-date']
    change_actions = ['view_booking_report']

    def get_urls(self):
        urls = super().get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return functools.update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urls.insert(
            0,
            path('<pk>/booking-report/', wrap(BookingReport.as_view()), name='%s_%s_booking_report' % info),
        )
        return urls

    def view_booking_report(self, request, obj):
        url = reverse('admin:%s_%s_booking_report' % (
            self.model._meta.app_label, self.model._meta.model_name,
        ), kwargs={'pk': obj.pk})
        return HttpResponseRedirect(url)
    view_booking_report.short_description = 'View booking report'
    view_booking_report.label = 'View booking report'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['event', 'archer']
    list_filter = ['event']
    autocomplete_fields = ['archer']


@admin.register(BookedSlot)
class BookedSlotAdmin(admin.ModelAdmin):
    list_display = ['start', 'end', 'target', 'distance', 'archer_names']
    list_filter = ['start', 'target']
    autocomplete_fields = ['archers']
    search_fields = ['start']

    def end(self, instance):
        return instance.end

    def archer_names(self, instance):
        return ', '.join(a.name for a in instance.archers.order_by('name'))


@admin.register(BookingTemplate)
class BookingTemplateAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['date', 'venue', 'start_times', 'target_setup']
    ordering = ['-date']
    actions = change_actions = ['create_next', 'update_from_coaching']

    def target_setup(self, instance):
        if instance.b_targets:
            return '%s + %s' % (instance.targets, instance.b_targets)
        return instance.targets

    @takes_instance_or_queryset
    def create_next(self, request, queryset):
        for template in queryset:
            template.create_next()
    create_next.short_description = 'Create next week'
    create_next.label = 'Create next week'

    @takes_instance_or_queryset
    def update_from_coaching(self, request, queryset):
        for template in queryset:
            template.update_from_coaching()
    update_from_coaching.short_description = 'Update from coaching'
    update_from_coaching.label = 'Update from coaching'
