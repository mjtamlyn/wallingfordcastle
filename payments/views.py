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
                try:
                    user = User.objects.get(customer_id=session.customer)
                except User.DoesNotExist:
                    return HttpResponse('ok - no such user')
            if session.mode == 'setup' and user.subscription_id:
                subscription = stripe.Subscription.retrieve(user.subscription_id)
                setup_intent = stripe.SetupIntent.retrieve(session.setup_intent)
                subscription.default_payment_method = setup_intent.payment_method
                subscription.save()
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
