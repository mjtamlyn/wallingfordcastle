from django import forms

from wallingford_castle.models import User
from .models import Entry


class EntryForm(forms.ModelForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields['drugs_consent'].required = True
        self.fields['gdpr_consent'].required = True

    class Meta:
        model = Entry
        fields = ['name', 'agb_number', 'club', 'date_of_birth', 'gender', 'bowstyle', 'notes', 'drugs_consent', 'gdpr_consent', 'future_event_consent']


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(email=email, password=password)
        user.tournament_only = True
        user.save()
        return user
