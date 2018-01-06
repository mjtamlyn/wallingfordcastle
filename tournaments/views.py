import json

from django.conf import settings
from django.contrib.auth import login
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView, FormView, TemplateView, UpdateView, View,
)

import requests
import stripe
from braces.views import LoginRequiredMixin, MessageMixin

from .forms import EntryForm, RegisterForm
from .models import Entry


class TournamentHome(TemplateView):
    template_name = 'tournaments/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            context['existing_entries'] = self.request.user.entry_set.all()
            context['to_pay'] = self.request.user.entry_set.filter(paid=False).count() * 15
            context['STRIPE_KEY'] = settings.STRIPE_KEY
            context['entry_form'] = EntryForm()
        else:
            context['register_form'] = RegisterForm()
        return context


class TournamentRegistration(FormView):
    template_name = 'register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tournaments:home')


class EntryCreate(LoginRequiredMixin, MessageMixin, CreateView):
    template_name = 'tournaments/entry_form.html'
    model = Entry
    form_class = EntryForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.messages.success('Entry added, please pay below.')
        response = super().form_valid(form)
        data = json.dumps({
            'icon_emoji': ':wave:',
            'text': 'New entry received for %s!\n%s' % (
                form.instance.name,
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
        return reverse('tournaments:home')


class EntryUpdate(LoginRequiredMixin, MessageMixin, UpdateView):
    template_name = 'tournaments/entry_form.html'
    model = Entry
    fields = ['name', 'agb_number', 'club', 'gender', 'bowstyle', 'notes']

    def get_object(self):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('tournaments:home')


class EntryDelete(LoginRequiredMixin, DeleteView):
    model = Entry

    def get_object(self):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('tournaments:home')


class Pay(LoginRequiredMixin, MessageMixin, View):
    def post(self, request, *args, **kwargs):
        token = request.POST['stripeToken']
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
        to_pay = self.request.user.entry_set.filter(paid=False).count() * 1500
        stripe.Charge.create(
            amount=to_pay,
            currency="GBP",
            description="Wallingford Castle Archers Tournament Fee",
            customer=customer.id,
            source=source.id,
        )
        to_pay = self.request.user.entry_set.update(paid=True)
        self.messages.success('Thanks! You will receive a confirmation email soon.')
        return redirect('tournaments:home')
