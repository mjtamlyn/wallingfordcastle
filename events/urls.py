from django.urls import path, register_converter

from . import api, views
from .converters import ApiDateConverter, SlotReferenceConverter

app_name = 'events'

register_converter(ApiDateConverter, 'date')
register_converter(SlotReferenceConverter, 'slot')

urlpatterns = [
    path('', views.EventList.as_view(), name='event-list'),
    path('<pk>/', views.BookEvent.as_view(), name='book-event'),
]

range_api_urlpatterns = [
    path('', api.date_list, name='date-list'),
    path('<date:date>/', api.date_slots, name='date-slots'),
    path('archers/', api.bookable_archers, name='bookable-archers'),
    path('group-booking-info/<slot:slot>/', api.group_booking_info, name='group-booking-info'),
    path('absentable-archers/<slot:slot>/', api.slot_absentable_archers, name='slot-absentable-archers'),
    path(
        'additional-bookable-archers/<slot:slot>/',
        api.slot_additional_bookable_archers,
        name='slot-additional-bookable-archers',
    ),
    # TODO: make book and cancel have slot details in the URL
    path('book/', api.book_slot, name='book-slot'),
    path('cancel/', api.cancel_slot, name='cancel-slot'),
    path('report-absence/<slot:slot>/', api.report_absence, name='report-absence'),
    path('book-in/<slot:slot>/', api.book_in, name='book-in'),
]
