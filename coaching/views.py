import json

from django.conf import settings
from django.db import transaction
from django.db.models.functions import Lower
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, FormView, TemplateView, View
from django.views.generic.detail import SingleObjectMixin

import requests
import stripe
from braces.views import MessageMixin

from payments.models import PaymentIntent
from records.models import Achievement
from wallingford_castle.mixins import FullMemberRequired
from wallingford_castle.models import Archer, Season

from .forms import TrialContinueForm
from .models import TrainingGroup, TrainingGroupType, Trial


class CurrentSeasonMixin(FullMemberRequired):
    def get_season(self):
        return self.get_current_season()

    def get_current_season(self):
        return Season.objects.get_current()

    def get_upcoming_season(self):
        return Season.objects.get_upcoming()

    def get_context_data(self, **kwargs):
        return super().get_context_data(season=self.get_season(), **kwargs)


class GroupsOverview(CurrentSeasonMixin, TemplateView):
    template_name = 'coaching/overview.html'

    def get_context_data(self, **kwargs):
        context = {}
        season = self.get_season()
        groups = TrainingGroup.objects.filter(
            season=season,
            coaches__in=Archer.objects.managed_by(self.request.user),
        ).order_by('session_day', 'session_start_time')
        context['coached_groups'] = groups
        if self.request.user.is_superuser:
            context['uncoached_groups'] = TrainingGroup.objects.filter(season=season).exclude(
                id__in=[g.id for g in groups],
            )
        upcoming = self.get_upcoming_season()
        if upcoming:
            upcoming_groups = TrainingGroup.objects.filter(
                season=upcoming,
                coaches__in=Archer.objects.managed_by(self.request.user),
            ).order_by('session_day', 'session_start_time')
            context.update(upcoming=upcoming, upcoming_groups=upcoming_groups)
            if self.request.user.is_superuser:
                context['upcoming_uncoached_groups'] = TrainingGroup.objects.filter(season=upcoming).exclude(
                    id__in=[g.id for g in upcoming_groups],
                )
        return super().get_context_data(**context, **kwargs)


class GroupMixin(CurrentSeasonMixin):
    context_object_name = 'group'
    model = TrainingGroup

    def get_object(self):
        season = self.get_season()
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
        return group


class GroupReport(GroupMixin, DetailView):
    template_name = 'coaching/group_report.html'
    schedule_url_name = 'group-schedule'

    def get_object(self):
        group = super().get_object()
        if self.request.user.is_superuser:
            return group
        if not (set(group.coaches.all()) & set(Archer.objects.managed_by(self.request.user))):
            raise Http404('You don\'t have access to this group')
        return group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.object
        context['archers'] = group.participants.order_by('name').select_related('user')
        context['current_trials'] = group.trial_set.filter_ongoing().order_by(
            'archer__name',
        ).select_related('archer__user')
        for archer in context['archers']:
            archer.best_outdoor = Achievement.objects.best_outdoor(archer)
            archer.best_portsmouth = Achievement.objects.best_portsmouth(archer)
            archer.best_wa_18 = Achievement.objects.best_wa_18(archer)
            archer.best_beginner = Achievement.objects.best_beginner(archer)
        context['schedule_url_name'] = 'coaching:' + self.schedule_url_name
        return context


class UpcomingGroupReport(GroupReport):
    schedule_url_name = 'upcoming-group-schedule'

    def get_season(self):
        return self.get_upcoming_season()


class GroupSchedule(GroupMixin, DetailView):
    template_name = 'coaching/group_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sessions'] = self.object.groupsession_set.order_by('start').filter(
            start__date__gte=timezone.now().date(),
        )
        context['is_coach'] = self.request.user in [
            archer.user for archer in self.object.coaches.all()
        ]
        return context


class UpcomingGroupSchedule(GroupSchedule):
    def get_season(self):
        return self.get_upcoming_season()


class TrialPayment(MessageMixin, View):
    def get(self, request, *args, **kwargs):
        customer_id = self.request.user.customer_id or None
        membership_overview_url = reverse('membership:overview')
        trials = Trial.objects.filter(
            archer__user=self.request.user,
            paid=False,
        )
        if not trials:
            self.messages.error('You have no trials to pay for.')
            return redirect(membership_overview_url)
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': '%s Archery Trial' % (trial.archer),
                    },
                    'unit_amount': trial.fee * 100,
                },
                'quantity': 1,
            } for trial in trials],
            mode='payment',
            customer=customer_id,
            customer_email=None if customer_id else self.request.user.email,
            success_url=request.build_absolute_uri(membership_overview_url),
            cancel_url=request.build_absolute_uri(membership_overview_url),
        )
        intent = PaymentIntent.objects.create(stripe_id=session.payment_intent, user=self.request.user)
        for trial in trials:
            intent.lineitemintent_set.create(item=trial)
        return redirect(session.url, status_code=303)


class TrialContinue(SingleObjectMixin, FormView):
    form_class = TrialContinueForm
    model = Trial
    pk_url_kwarg = 'trial_pk'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['trial'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            member = form.save()
            if settings.SLACK_MEMBERSHIP_HREF:
                data = json.dumps({
                    'icon_emoji': ':thumbsup:',
                    'text': '%s has joined after their trial!\n%s' % (
                        form.cleaned_data['name'],
                        self.request.build_absolute_uri(
                            reverse(
                                'admin:wallingford_castle_membershipinterest_change',
                                args=(form.instance.pk,),
                            )
                        ),
                    )
                })
                try:
                    requests.post(settings.SLACK_MEMBERSHIP_HREF, data=data)
                except Exception:
                    pass
            customer_id = self.request.user.customer_id or None
            if not self.request.user.subscription_id:
                membership_overview_url = reverse('membership:overview')
                session = stripe.checkout.Session.create(
                    line_items=[{'price': price['id'], 'quantity': 1} for price in member.prices],
                    mode='subscription',
                    customer=customer_id,
                    customer_email=None if customer_id else self.request.user.email,
                    success_url=self.request.build_absolute_uri(membership_overview_url),
                    cancel_url=self.request.build_absolute_uri(membership_overview_url),
                )
                return redirect(session.url, status_code=303)
            else:
                self.request.user.update_subscriptions()
