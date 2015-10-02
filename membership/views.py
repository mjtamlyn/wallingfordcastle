import json

from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, View

from braces.views import LoginRequiredMixin, MessageMixin
import requests
import stripe

from .forms import MemberForm


class Overview(LoginRequiredMixin, TemplateView):
    template_name = 'membership/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = self.request.user.members.all()
        context['monthly_fee'] = sum(member.plan_cost for member in context['members'])
        context['STRIPE_KEY'] = settings.STRIPE_KEY
        return context


class MemberUpdate(LoginRequiredMixin, MessageMixin, UpdateView):
    template_name = 'membership/member-update.html'
    form_class = MemberForm
    pk_url_kwarg = 'member_id'
    success_url = reverse_lazy('membership:overview')

    def get_queryset(self):
        return self.request.user.members.all()

    def get_object(self):
        obj = super().get_object()
        self.original_plan = obj.plan
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.plan != self.original_plan:
            if self.object.subscription_id:
                customer = stripe.Customer.retrieve(self.request.user.customer_id)
                subscription = customer.subscriptions.retrieve(self.object.subscription_id)
                subscription.plan = self.object.plan
                subscription.save()
        self.messages.success('Details successfully updated!')
        if settings.SLACK_MEMBERSHIP_HREF:
            data = json.dumps({
                'icon_emoji': ':exclamation:',
                'text': '%s has updated details!\n%s' % (
                    form.cleaned_data['name'],
                    self.request.build_absolute_uri(
                        reverse(
                            'admin:membership_member_change',
                            args=(form.instance.pk,),
                        )
                    ),
                )
            })
            try:
                requests.post(settings.SLACK_MEMBERSHIP_HREF, data=data)
            except Exception:
                pass
        return response


class PaymentDetails(View):
    def post(self, request, *args, **kwargs):
        token = request.POST['stripeToken']
        if self.request.user.customer_id:
            customer = stripe.Customer.retrieve(self.request.user.customer_id)
            source = customer.sources.create(source=token)
            customer.default_source = source
            customer.save()
        else:
            customer = stripe.Customer.create(
                source=token,
                email=self.request.user.email,
            )
            self.request.user.customer_id = customer.id
            self.request.user.save()
        for member in self.request.user.members.filter(subscription_id=''):
            subscription = customer.subscriptions.create(plan=member.plan)
            member.subscription_id = subscription.id
            member.save()
        return HttpResponseRedirect(reverse('membership:overview'))
