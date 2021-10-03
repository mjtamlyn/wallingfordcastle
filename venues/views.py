from django.views.generic import DetailView, ListView

from .models import Venue


class VenueList(ListView):
    template_name = 'venues/venue_list.html'
    model = Venue

    def get_queryset(self):
        return Venue.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        indoor = []
        outdoor = []
        for venue in self.object_list:
            if venue.season == 'indoor':
                indoor.append(venue)
            else:
                outdoor.append(venue)
        context.update(indoor=indoor, outdoor=outdoor)
        return context


class VenueDetail(DetailView):
    template_name = 'venues/venue_detail.html'
    model = Venue

    def get_queryset(self):
        return Venue.objects.filter(active=True)
