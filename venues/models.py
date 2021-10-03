from django.db import models

INDOOR_OUTDOOR = (
    ('indoor', 'Indoor'),
    ('outdoor', 'Outdoor'),
)


class Venue(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    google_maps_link = models.URLField()
    season = models.CharField(max_length=20, choices=INDOOR_OUTDOOR)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
