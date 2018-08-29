import json

from django.conf import settings
from django.views.generic import TemplateView, CreateView
from django.urls import reverse, reverse_lazy

from braces.views import MessageMixin
import requests

from courses.forms import MinisInterestForm
from .forms import MembershipInterestForm


class HomeView(MessageMixin, TemplateView):
    template_name = 'home.html'


class Join(TemplateView): 
    template_name = 'join.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['membership_form'] = MembershipInterestForm()
        return context


class Juniors(TemplateView):
    template_name = 'juniors.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['minis_form'] = MinisInterestForm()
        return context


class MembershipInterestView(MessageMixin, CreateView):
    form_class = MembershipInterestForm
    template_name = 'membership_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.messages.success('Thanks for your interest! We will be in touch soon.')
        if settings.SLACK_MEMBERSHIP_HREF:
            data = json.dumps({
                'icon_emoji': ':wave:',
                'text': 'New membership interest received for %s!\n%s' % (
                    form.cleaned_data['name'],
                    self.request.build_absolute_uri(
                        reverse(
                            'admin:wallingford_castle_membershipinterest_change',
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


class Venues(TemplateView):
    template_name = 'venues.html'
