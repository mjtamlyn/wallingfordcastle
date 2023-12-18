import json

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, View

import requests
import stripe
from braces.views import MessageMixin

from payments.models import Checkout

from .forms import BeginnersInterestForm
from .models import BeginnersCourse


class BeginnersIndex(TemplateView):
    template_name = 'beginners/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beginners_form'] = BeginnersInterestForm()
        context['current_courses'] = BeginnersCourse.objects.current()
        context['upcoming_courses'] = BeginnersCourse.objects.upcoming().order_by('counter')
        return context


class BeginnersInterestView(MessageMixin, CreateView):
    form_class = BeginnersInterestForm
    template_name = 'membership_form.html'
    success_url = reverse_lazy('beginners:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.messages.success('Thanks for your interest! We will be in touch soon.')
        if settings.SLACK_BEGINNERS_HREF:
            data = json.dumps({
                'icon_emoji': ':wave:',
                'text': 'New beginners course interest received for %s!\n%s' % (
                    form.cleaned_data['name'],
                    self.request.build_absolute_uri(
                        reverse(
                            'admin:beginners_beginner_change',
                            args=(form.instance.pk,),
                        )
                    ),
                )
            })
            try:
                requests.post(settings.SLACK_BEGINNERS_HREF, data=data)
            except Exception:
                pass
        return response


class Payment(MessageMixin, View):
    def get(self, request, *args, **kwargs):
        customer_id = self.request.user.customer_id or None
        membership_overview_url = reverse('membership:overview')
        beginners = self.request.user.beginner_set.filter(paid=False)
        if not beginners:
            self.messages.error('You have no beginners to pay for.')
            return redirect(membership_overview_url)
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': '%s Beginners Course' % (beginner),
                    },
                    'unit_amount': beginner.fee * 100,
                },
                'quantity': 1,
            } for beginner in beginners],
            mode='payment',
            customer=customer_id,
            customer_email=None if customer_id else self.request.user.email,
            customer_creation='always',
            success_url=request.build_absolute_uri(membership_overview_url),
            cancel_url=request.build_absolute_uri(membership_overview_url),
        )
        intent = Checkout.objects.create(stripe_id=session.id, user=self.request.user)
        for beginner in beginners:
            intent.lineitemintent_set.create(item=beginner)
        return redirect(session.url, status_code=303)
