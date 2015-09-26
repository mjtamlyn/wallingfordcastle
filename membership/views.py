from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin


class Overview(LoginRequiredMixin, TemplateView):
    template_name = 'membership/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = self.request.user.members.all()
        return context
