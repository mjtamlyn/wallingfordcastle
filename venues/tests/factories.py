import factory
import factory.django

from ..models import Venue


class VenueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Venue
