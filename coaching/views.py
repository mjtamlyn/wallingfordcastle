from django.db.models.functions import Lower
from django.http import Http404
from django.views.generic import DetailView, TemplateView

from records.models import Achievement
from wallingford_castle.mixins import FullMemberRequired
from wallingford_castle.models import Archer, Season

from .models import TrainingGroup, TrainingGroupType


class CurrentSeasonMixin(FullMemberRequired):
    def get_current_season(self):
        return Season.objects.get_current()

    def get_context_data(self, **kwargs):
        return super().get_context_data(season=self.get_current_season(), **kwargs)


class GroupsOverview(CurrentSeasonMixin, TemplateView):
    template_name = 'coaching/overview.html'

    def get_context_data(self, **kwargs):
        season = self.get_current_season()
        groups = TrainingGroup.objects.filter(
            season=season,
            coaches__in=Archer.objects.managed_by(self.request.user),
        )
        return super().get_context_data(coached_groups=groups, **kwargs)


class GroupReport(CurrentSeasonMixin, DetailView):
    template_name = 'coaching/group_report.html'
    context_object_name = 'group'
    model = TrainingGroup

    def get_object(self):
        season = self.get_current_season()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day, level = self.kwargs['group'].split('-', 1)
        names = map(lambda s: s.replace('_', ' '), level.split('-'))
        levels = TrainingGroupType.objects.annotate(name_lower=Lower('name')).filter(name_lower__in=names)
        possible_groups = TrainingGroup.objects.filter(season=season).filter(
            session_day=days.index(day),
        )
        if len(possible_groups) > 1:
            group = None
            for candidate in possible_groups:
                if set(candidate.level.all()) == set(levels):
                    group = candidate
                    break
            if not group:
                raise Http404('No group found')
        elif len(possible_groups) == 1:
            group = possible_groups[0]
        else:
            raise Http404('No group found')
        if not (set(group.coaches.all()) & set(Archer.objects.managed_by(self.request.user))):
            raise Http404('You don\'t have access to this group')
        return group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.object
        context['archers'] = group.participants.order_by('name')
        for archer in context['archers']:
            archer.best_outdoor = Achievement.objects.best_outdoor(archer)
            archer.best_portsmouth = Achievement.objects.best_portsmouth(archer)
            archer.best_wa_18 = Achievement.objects.best_wa_18(archer)
            archer.best_beginner = Achievement.objects.best_beginner(archer)
        return context
