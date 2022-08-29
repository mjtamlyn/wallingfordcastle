from django import forms

from archery.bows import BOWSTYLE_CHOICES
from wallingford_castle.forms import DirectRegisterForm

from .models import Entry


class EntryForm(forms.ModelForm):
    def __init__(self, tournament, **kwargs):
        self.tournament = tournament
        super().__init__(**kwargs)
        self.fields['drugs_consent'].required = True
        self.fields['gdpr_consent'].required = True
        self.fields['bowstyle'].choices = [('', '---------')] + list(
            filter(lambda c: c[0] in self.tournament.bowstyles, BOWSTYLE_CHOICES)
        )
        self.fields['round'].choices = [('', '---------')] + [
            (r.pk, r.name) for r in self.tournament.rounds.all()
        ]
        if len(self.fields['round'].choices) == 2:
            self.fields['round'].choices = [self.fields['round'].choices[-1]]
            self.fields['round'].initial = self.fields['round'].choices[-1][0]
            self.fields['round'].disabled = True
        else:
            self.fields['round'].required = True

    class Meta:
        model = Entry
        fields = [
            'name',
            'agb_number',
            'club',
            'date_of_birth',
            'round',
            'gender',
            'bowstyle',
            'notes',
            'drugs_consent',
            'gdpr_consent',
            'future_event_consent',
        ]

    def save(self, **kwargs):
        self.instance.tournament = self.tournament
        if self.tournament.waiting_list_enabled:
            self.instance.waiting_list = True
        super().save(**kwargs)


class SeriesEntryForm(EntryForm):
    def save(self, **kwargs):
        series = self.tournament
        if series.waiting_list_enabled:
            self.instance.waiting_list = True
        self.instance.series_entry = True
        for tournament in series.tournament_set.all():
            self.instance.pk = None
            self.instance.tournament = tournament
            self.instance.save()
        super(forms.ModelForm, self).save(**kwargs)


class RegisterForm(DirectRegisterForm):

    def save(self):
        user = super().save()
        user.tournament_only = True
        user.save()
        return user
