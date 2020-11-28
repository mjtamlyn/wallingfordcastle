import json

from django.conf import settings
from django.contrib.auth import login
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, FormView, TemplateView, UpdateView, View,
)

import requests
import stripe
from braces.views import LoginRequiredMixin, MessageMixin

from events.models import Event

from .forms import EntryForm, RegisterForm
from .models import Entry, Tournament


class TournamentList(TemplateView):
    template_name = 'tournaments/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        now = timezone.now()
        context['upcoming_tournaments'] = Tournament.objects.filter(date__gt=now).order_by('date')
        context['past_tournaments'] = Tournament.objects.filter(date__lte=now).order_by('-date')
        context['bookable_events'] = Event.objects.filter(bookable=True, date__gt=now).order_by('date')
        return context


class TournamentMixin():
    def get_tournament(self):
        return get_object_or_404(Tournament, slug=self.kwargs['tournament_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.tournament = self.get_tournament()
        context['tournament'] = self.tournament
        return context


class TournamentDetail(TournamentMixin, TemplateView):
    template_name = 'tournaments/tournament_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            context['existing_entries'] = self.request.user.entry_set.filter(tournament=self.tournament)
            context['to_pay'] = self.request.user.entry_set.filter(
                paid=False,
                tournament=self.tournament,
            ).count() * self.tournament.entry_fee
            context['STRIPE_KEY'] = settings.STRIPE_KEY
            context['entry_form'] = EntryForm()
        else:
            context['register_form'] = RegisterForm()
        return context


class TournamentRegistration(TournamentMixin, FormView):
    template_name = 'tournaments/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_tournament().get_absolute_url()


class EntryCreate(LoginRequiredMixin, TournamentMixin, MessageMixin, CreateView):
    template_name = 'tournaments/entry_form.html'
    model = Entry
    form_class = EntryForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.tournament = self.get_tournament()
        self.messages.success('Entry added, please pay below.')
        response = super().form_valid(form)
        data = json.dumps({
            'icon_emoji': ':wave:',
            'text': 'New entry received for %s to %s!\n%s' % (
                form.instance.name,
                form.instance.tournament,
                self.request.build_absolute_uri(
                    reverse(
                        'admin:tournaments_entry_change',
                        args=(form.instance.pk,),
                    )
                ),
            )
        })
        try:
            requests.post(settings.SLACK_TOURNAMENT_HREF, data=data)
        except Exception:
            pass
        return response

    def get_success_url(self):
        return self.get_tournament().get_absolute_url()


class EntryUpdate(LoginRequiredMixin, TournamentMixin, MessageMixin, UpdateView):
    template_name = 'tournaments/entry_form.html'
    model = Entry
    fields = [
        'name',
        'agb_number',
        'club',
        'date_of_birth',
        'gender',
        'bowstyle',
        'notes',
        'drugs_consent',
        'gdpr_consent',
        'future_event_consent',
    ]

    def get_object(self):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return self.get_tournament().get_absolute_url()


class EntryDelete(LoginRequiredMixin, TournamentMixin, DeleteView):
    model = Entry

    def get_object(self):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return self.get_tournament().get_absolute_url()


class Pay(LoginRequiredMixin, TournamentMixin, MessageMixin, View):
    def post(self, request, *args, **kwargs):
        token = request.POST['stripeToken']
        tournament = self.get_tournament()
        if self.request.user.customer_id:
            customer = stripe.Customer.retrieve(self.request.user.customer_id)
            source = customer.sources.create(source=token)
            customer.save()
        else:
            customer = stripe.Customer.create(
                email=self.request.user.email,
            )
            source = customer.sources.create(source=token)
            self.request.user.customer_id = customer.id
            self.request.user.save()
        to_pay = self.request.user.entry_set.filter(
            paid=False,
            tournament=tournament,
        ).count() * 100 * tournament.entry_fee
        stripe.Charge.create(
            amount=to_pay,
            currency="GBP",
            description="Wallingford Castle Archers Tournament Fee",
            customer=customer.id,
            source=source.id,
        )
        to_pay = self.request.user.entry_set.filter(tournament=tournament).update(paid=True)
        self.messages.success('Thanks! You will receive a confirmation email soon.')
        return redirect(tournament.get_absolute_url())
