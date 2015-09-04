import json

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, CreateView

from braces.views import MessageMixin
import requests

from .forms import MembershipInterestForm, BeginnersCourseForm


class HomeView(MessageMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['membership_form'] = MembershipInterestForm()
        context['beginners_form'] = BeginnersCourseForm()
        return context


class MembershipInterestView(MessageMixin, CreateView):
    form_class = MembershipInterestForm
    template_name = 'membership_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.messages.success('Thanks for your interest! We will be in touch soon.')
        if settings.SLACK_MEMBERSHIP_HREF:
            data = json.dumps({
                'icon_emoji': ':wave:',
                'text': 'New membership interest received for %s!' % form.cleaned_data['name'],
            })
            try:
                requests.post(settings.SLACK_MEMBERSHIP_HREF, data=data)
            except Exception:
                pass
        return super().form_valid(form)


class BeginnersCourseView(MessageMixin, CreateView):
    form_class = BeginnersCourseForm
    template_name = 'membership_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.messages.success('Thanks for your interest! We will be in touch soon.')
        if settings.SLACK_BEGINNERS_HREF:
            data = json.dumps({
                'icon_emoji': ':wave:',
                'text': 'New beginners course interest received for %s!' % form.cleaned_data['name'],
            })
            try:
                requests.post(settings.SLACK_BEGINNERS_HREF, data=data)
            except Exception:
                pass
        return super().form_valid(form)
