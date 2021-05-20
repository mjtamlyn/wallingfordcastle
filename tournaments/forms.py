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


class RegisterForm(DirectRegisterForm):

    def save(self):
        user = super().save()
        user.tournament_only = True
        user.save()
        return user
