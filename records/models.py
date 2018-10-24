from django.db import models

from wallingford_castle.models import Archer

from .badges import BADGE_CHOICES, BADGE_GROUP_CHOICES


class Achievement(models.Model):
    archer = models.ForeignKey(Archer, on_delete=models.CASCADE)
    date_awarded = models.DateField(blank=True, null=True)
    badge = models.CharField(max_length=31, choices=BADGE_CHOICES)
    badge_group = models.CharField(max_length=31, choices=BADGE_GROUP_CHOICES)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return 'Archer %s achieved %s' % (self.archer_id, self.get_badge_display())
