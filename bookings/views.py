from django.views.generic import TemplateView


class BookingsIndex(TemplateView):
    template_name = 'bookings/index.html'
