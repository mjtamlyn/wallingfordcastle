import json

from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView

from braces.views import MessageMixin
import requests

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
