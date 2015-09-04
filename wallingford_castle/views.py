from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, CreateView

from braces.views import MessageMixin

from .forms import MembershipInterestForm


class HomeView(MessageMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['membership_form'] = MembershipInterestForm()
        return context


class MembershipInterestView(MessageMixin, CreateView):
    form_class = MembershipInterestForm
    template_name = 'membership_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.messages.success('Thanks for your interest! We will be in touch soon.')
        return super().form_valid(form)
