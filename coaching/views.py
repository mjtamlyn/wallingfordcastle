import json

from django.conf import settings
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, FormView, TemplateView, View
from django.views.generic.detail import SingleObjectMixin

import requests
import stripe
from braces.views import MessageMixin

from payments.models import Checkout
from records.models import Achievement
from wallingford_castle.mixins import FullMemberRequired
from wallingford_castle.models import Archer, Season

from .forms import TrialContinueForm
from .models import ArcherSeason, TrainingGroup, Trial


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
        if groups:
            context['uncoached_groups'] = TrainingGroup.objects.filter(season=season).exclude(
                id__in=[g.id for g in groups],
            ).order_by('session_day', 'session_start_time')
        upcoming = self.get_upcoming_season()
        if upcoming:
            upcoming_groups = TrainingGroup.objects.filter(
                season=upcoming,
                coaches__in=Archer.objects.managed_by(self.request.user),
            ).order_by('session_day', 'session_start_time')
            context.update(upcoming=upcoming, upcoming_groups=upcoming_groups)
            if upcoming_groups:
                context['upcoming_uncoached_groups'] = TrainingGroup.objects.filter(season=upcoming).exclude(
                    id__in=[g.id for g in upcoming_groups],
                ).order_by('session_day', 'session_start_time')
        return super().get_context_data(**context, **kwargs)


class GroupMixin(CurrentSeasonMixin):
    context_object_name = 'group'
    model = TrainingGroup

    def get_queryset(self):
        season = self.get_season()
        return super().get_queryset().filter(season=season)


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
    slug_url_kwarg = None

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
            customer_creation=None if customer_id else 'always',
            success_url=request.build_absolute_uri(membership_overview_url),
            cancel_url=request.build_absolute_uri(membership_overview_url),
        )
        intent = Checkout.objects.create(stripe_id=session.id, user=self.request.user)
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
                                'admin:membership_member_change',
                                args=(member.pk,),
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
                    customer_creation=None if customer_id else 'always',
                    success_url=self.request.build_absolute_uri(membership_overview_url),
                    cancel_url=self.request.build_absolute_uri(membership_overview_url),
                )
                return redirect(session.url, status_code=303)
            else:
                self.request.user.update_subscriptions()
                return redirect('membership:overview')


class EventPlan(FullMemberRequired, MessageMixin, TemplateView):
    template_name = 'coaching/event_plan.html'

    def dispatch(self, request, *args, **kwargs):
        archer = get_object_or_404(Archer, pk=kwargs['archer_id'])
        if (
                archer.user_id != request.user.pk and request.user not in archer.managing_users.all() and
                not request.user.is_superuser
        ):
            self.messages.error('You do not have access rights to this plan')
            return redirect('membership:overview')
        current_season = self.get_season()
        try:
            self.plan = ArcherSeason.objects.get(archer=archer, season=current_season)
        except ArcherSeason.DoesNotExist:
            self.messages.error('We do not have an event plan for that archer at this time.')
            return redirect('membership:overview')
        return super().dispatch(request, *args, **kwargs)

    def get_season(self):
        return Season.objects.get_current()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan'] = self.plan
        return context


class NextEventPlan(EventPlan):
    def get_season(self):
        return Season.objects.get_next()
