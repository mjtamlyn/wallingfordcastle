from django.db import models

from wallingford_castle.models import Archer

from .badges import (
    BADGE_CHOICES, BADGE_GROUP_CHOICES, BADGE_LOOKUP, CLUB_OUTDOOR_250,
    CLUB_PORTSMOUTH, CLUB_WA_18, WA_BEGINNERS,
)


class AchievementManager(models.Manager):
    def _best_badge(self, archer, category):
        achievements = self.filter(archer=archer, badge_group=category.slug)
        if not achievements:
            return None
        return max(BADGE_LOOKUP[ach.badge] for ach in achievements)

    def best_outdoor(self, archer):
        return self._best_badge(archer, CLUB_OUTDOOR_250)

    def best_wa_18(self, archer):
        return self._best_badge(archer, CLUB_WA_18)

    def best_portsmouth(self, archer):
        return self._best_badge(archer, CLUB_PORTSMOUTH)

    def best_beginner(self, archer):
        return self._best_badge(archer, WA_BEGINNERS)


class Achievement(models.Model):
    archer = models.ForeignKey(Archer, on_delete=models.CASCADE)
    date_awarded = models.DateField(blank=True, null=True)
    badge = models.CharField(max_length=31, choices=BADGE_CHOICES)
    badge_group = models.CharField(max_length=31, choices=BADGE_GROUP_CHOICES)
    paid = models.BooleanField(default=False)

    objects = AchievementManager()

    def __str__(self):
        return 'Archer %s achieved %s' % (self.archer_id, self.get_badge_display())
