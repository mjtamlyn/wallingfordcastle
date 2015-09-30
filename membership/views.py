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
        context['STRIPE_KEY'] = settings.STRIPE_KEY
        return context


class MemberUpdate(LoginRequiredMixin, MessageMixin, UpdateView):
    template_name = 'membership/member-update.html'
    form_class = MemberForm
    pk_url_kwarg = 'member_id'
    success_url = reverse_lazy('membership:overview')

    def get_queryset(self):
        return self.request.user.members.all()

    def form_valid(self, form):
        response = super().form_valid(form)
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
        stripe.api_key = settings.STRIPE_SECRET_KEY
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
        return HttpResponseRedirect(reverse('membership:overview'))
