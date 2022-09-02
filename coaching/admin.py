import datetime
import functools

from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils import timezone
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

from django_object_actions import DjangoObjectActions

from wallingford_castle.admin import ArcherDataMixin

from .models import GroupSession, TrainingGroup, TrainingGroupType, Trial


class CreateSessionsForm(forms.Form):
    def __init__(self, training_group, **kwargs):
        super().__init__(**kwargs)
        self.training_group = training_group
        sessions = training_group.groupsession_set.all()
        session_lookup = {session.start.date(): session for session in sessions}
        today = timezone.now().date()
        self.possible_dates = training_group.possible_dates(after=today)
        for i, date in enumerate(self.possible_dates):
            if date in session_lookup:
                continue
            self.fields['cancel_%s' % i] = forms.CharField(
                label=date.strftime('%A %-d %B %Y'),
                required=False,
            )

    def save(self):
        for i, date in enumerate(self.possible_dates):
            self.training_group.groupsession_set.create(
                start=datetime.datetime.combine(date, self.training_group.session_start_time, tzinfo=settings.TZ),
                cancelled_because=self.cleaned_data['cancel_%s' % i],
            )


class CreateSessionsView(SingleObjectMixin, FormView):
    model = TrainingGroup
    form_class = CreateSessionsForm
    template_name = 'admin/coaching/traininggroup/create_sessions.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['training_group'] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = TrainingGroup._meta
        context['title'] = 'Create sessions'
        context['sessions'] = self.object.groupsession_set.order_by('start')
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name),
            args=(self.object.pk,),
        )


@admin.register(TrainingGroup)
class TrainingGroupAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['group_name', 'season', 'time', 'number_of_archers', 'current_trials']
    list_filter = ['season', 'level']
    autocomplete_fields = ['coaches', 'participants']
    change_actions = ['create_sessions', 'bill_participants']
    search_fields = ['level__name']

    def number_of_archers(self, instance):
        return instance.participants.count()

    def current_trials(self, instance):
        return instance.trial_set.filter_ongoing().count()

    def get_urls(self):
        urls = super().get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return functools.update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urls.insert(
            0,
            path('<int:pk>/create-sessions/', wrap(CreateSessionsView.as_view()), name='%s_%s_create_sessions' % info),
        )
        return urls

    def create_sessions(self, request, instance):
        url = reverse(
            'admin:%s_%s_create_sessions' % (self.model._meta.app_label, self.model._meta.model_name),
            kwargs={'pk': instance.pk},
        )
        return HttpResponseRedirect(url)

    def bill_participants(self, request, instance):
        errors = []
        for archer in instance.participants.all():
            if not archer.user.customer_id or not archer.user.subscription_id:
                errors.append(archer.name)
        if errors:
            for archer in errors:
                messages.error(request, '%s does not have an active subscription' % archer)
            return

        url = (
            reverse('admin:wallingford_castle_archer_invoice_item') +
            '?ids=%s' % ','.join(str(archer.pk) for archer in instance.participants.all())
        )
        return HttpResponseRedirect(url)


@admin.register(TrainingGroupType)
class TrainingGroupTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'age_group']


@admin.register(GroupSession)
class GroupSessionAdmin(admin.ModelAdmin):
    list_display = ['start', 'group', 'cancelled_because']
    list_filter = ['group']
    ordering = ['start']
    autocomplete_fields = ['group', 'booked_slot']


class TrialStatusListFilter(admin.SimpleListFilter):
    title = 'status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('future', 'Future'),
            ('in-progress', 'In progress'),
            ('joined', 'Joined'),
            ('completed', 'Completed'),
        )

    def queryset(self, request, queryset):
        today = timezone.now()
        if self.value() == 'future':
            return queryset.filter(session_1__gt=today)
        if self.value() == 'in-progress':
            return queryset.filter(session_1__lt=today, session_4__gt=today)
        if self.value() == 'completed':
            return queryset.filter(session_4__lt=today, archer__member__isnull=True)
        if self.value() == 'joined':
            return queryset.filter(session_4__lt=today, archer__member__isnull=False)


@admin.register(Trial)
class TrialAdmin(ArcherDataMixin, admin.ModelAdmin):
    list_display = ['archer', 'status', 'paid', 'group', 'session_1']
    list_filter = [TrialStatusListFilter]
    readonly_fields = ['archer_email', 'archer_age_group', 'archer_contact_number']

    def status(self, instance):
        today = timezone.now()
        if instance.session_1 > today:
            return 'Future'
        elif instance.session_4 > today:
            return 'In progress'
        elif instance.archer.member_set.exists():
            return 'Joined'
        return 'Completed'
