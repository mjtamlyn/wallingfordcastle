from django import forms

from .models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name', 'agb_number', 'club', 'gender', 'bowstyle', 'notes']
