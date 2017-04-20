from django.http import Http404
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView, FormView, TemplateView, UpdateView,
)

from braces.views import LoginRequiredMixin, MessageMixin

from .models import Entry


class TournamentHome(TemplateView):
    template_name = 'tournaments/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['existing_entries'] = self.request.user.entry_set.all()
        context['to_pay'] = self.request.user.entry_set.filter(paid=False).count() * 15
        return context


class TournamentRegistration(FormView):
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EntryCreate(LoginRequiredMixin, MessageMixin, CreateView):
    template_name = 'tournaments/entry_form.html'
    model = Entry
    fields = ['name', 'agb_number', 'club', 'gender', 'bowstyle', 'notes']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tournaments:home')


class EntryUpdate(LoginRequiredMixin, MessageMixin, UpdateView):
    template_name = 'tournaments/entry_form.html'
    model = Entry
    fields = ['name', 'agb_number', 'club', 'gender', 'bowstyle', 'notes']

    def get_object(self):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('tournaments:home')


class EntryDelete(LoginRequiredMixin, DeleteView):
    model = Entry

    def get_object(self):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('tournaments:home')


class Pay(FormView):
    pass
