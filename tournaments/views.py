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
from membership.models import Member
from payments.models import PaymentIntent

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
                waiting_list=False,
                tournament=self.tournament,
            ).count() * self.tournament.entry_fee
            context['entry_form'] = EntryForm(tournament=self.tournament)
            if not self.request.user.tournament_only:
                context['members'] = Member.objects.managed_by(self.request.user)
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tournament'] = self.get_tournament()
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.tournament.waiting_list_enabled:
            self.messages.success('Entry added to waiting list. We hope to be in touch soon!')
        else:
            self.messages.success('Entry added, please pay below.')
        response = super().form_valid(form)
        data = json.dumps({
            'icon_emoji': ':wave:',
            'text': 'New entry received for %s to %s!%s\n%s' % (
                form.instance.name,
                form.instance.tournament,
                ' (waiting list)' if form.instance.tournament.waiting_list_enabled else '',
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
    def get(self, request, *args, **kwargs):
        tournament = self.get_tournament()
        customer_id = self.request.user.customer_id or None
        entries_to_pay_for = self.request.user.entry_set.filter(
            paid=False,
            tournament=tournament,
        )
        if not entries_to_pay_for:
            self.messages.error('You have no entries to pay for.')
            return redirect(tournament.get_absolute_url())
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': '%s entry to %s' % (entry, tournament),
                    },
                    'unit_amount': tournament.entry_fee * 100,
                },
                'quantity': 1,
            } for entry in entries_to_pay_for],
            mode='payment',
            customer=customer_id,
            customer_email=None if customer_id else self.request.user.email,
            success_url=request.build_absolute_uri(
                reverse('tournaments:pay-success', kwargs={'tournament_slug': tournament.slug}),
            ),
            cancel_url=request.build_absolute_uri(tournament.get_absolute_url()),
        )
        intent = PaymentIntent.objects.create(stripe_id=session.payment_intent, user=request.user)
        for entry in entries_to_pay_for:
            intent.lineitemintent_set.create(item=entry)
        return redirect(session.url, status_code=303)


class PaymentSuccess(LoginRequiredMixin, TournamentMixin, TemplateView):
    template_name = 'tournaments/payment_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tournament'] = self.get_tournament()
        return context
