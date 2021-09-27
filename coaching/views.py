from django.views.generic import TemplateView

from wallingford_castle.models import Archer, Season

from .models import TrainingGroup


class GroupsOverview(TemplateView):
    template_name = 'coaching/overview.html'

    def get_context_data(self, **kwargs):
        season = Season.objects.get_current()
        groups = TrainingGroup.objects.filter(
            season=season,
            coaches__in=Archer.objects.managed_by(self.request.user),
        )
        return super().get_context_data(season=season, coached_groups=groups, **kwargs)
