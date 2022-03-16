import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

import stripe

from .models import PaymentIntent


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhook(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        event = stripe.Event.construct_from(data, key=stripe.api_key)
        if event.type == 'payment_intent.succeeded':
            intent = PaymentIntent.objects.get(stripe_id=event.data.object.id)
            intent.mark_as_paid()
            if not intent.user.customer_id:
                intent.user.customer_id = event.data.object.customer
                intent.user.save()
            # TODO: Update customer
        return HttpResponse('ok')
