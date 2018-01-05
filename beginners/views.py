import json

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, View
from django.urls import reverse, reverse_lazy

from braces.views import MessageMixin
import requests
import stripe

from .forms import BeginnersInterestForm


class BeginnersInterestView(MessageMixin, CreateView):
    form_class = BeginnersInterestForm
    template_name = 'membership_form.html'
    success_url = reverse_lazy('home')

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
    def post(self, request, *args, **kwargs):
        token = request.POST['stripeToken']
        if self.request.user.customer_id:
            customer = stripe.Customer.retrieve(self.request.user.customer_id)
            source = customer.sources.create(source=token)
            customer.default_source = source.id
            customer.save()
        else:
            customer = stripe.Customer.create(
                source=token,
                email=self.request.user.email,
            )
            self.request.user.customer_id = customer.id
            self.request.user.save()
        beginners = self.request.user.beginner_set.filter(paid=False)
        amount = sum(beginner.fee for beginner in beginners)
        charge = stripe.Charge.create(
            amount=amount * 100,
            currency='gbp',
            customer=customer.id,
            description='Beginners course at Wallingford Castle Archers',
        )
        beginners.update(invoice_id=charge.id, paid=True)
        self.messages.success('Thanks! You will receive a confirmation email soon.')
        return HttpResponseRedirect(reverse('membership:overview'))
