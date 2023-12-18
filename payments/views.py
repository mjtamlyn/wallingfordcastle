import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

import stripe

from wallingford_castle.models import User

from .models import Checkout


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhook(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        event = stripe.Event.construct_from(data, key=stripe.api_key)
        if event.type == 'checkout.session.completed':
            session = event.data.object
            try:
                user = User.objects.get(email=session.customer_email)
            except User.DoesNotExist:
                return HttpResponse('ok - no such user')
            user.customer_id = session.customer
            if session.subscription:
                user.subscription_id = session.subscription
            try:
                intent = Checkout.objects.get(stripe_id=event.data.object.id)
                intent.mark_as_paid()
            except Checkout.DoesNotExist:
                pass
            user.save()
        return HttpResponse('ok')
