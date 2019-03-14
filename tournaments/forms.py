from django import forms

from wallingford_castle.models import User
from wallingford_castle.forms import DirectRegisterForm

from .models import Entry


class EntryForm(forms.ModelForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields['drugs_consent'].required = True
        self.fields['gdpr_consent'].required = True

    class Meta:
        model = Entry
        fields = ['name', 'agb_number', 'club', 'date_of_birth', 'gender', 'bowstyle', 'notes', 'drugs_consent', 'gdpr_consent', 'future_event_consent']


class RegisterForm(DirectRegisterForm):

    def save(self):
        user = super().save()
        user.tournament_only = True
        user.save()
        return user
