import floppyforms.__future__ as forms

from .models import Beginner


class BeginnersInterestForm(forms.ModelForm):
    def __init__(self, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(**kwargs)
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['date_of_birth'].required = True
        self.fields['experience'].label = 'Tell us about any archery you have done before'
        self.fields['experience'].help_text = 'No experience is necessary!'
        self.fields['notes'].label = (
            'Please tell us about any injuries or health problems, or anything else you think we should know'
        )

    def clean(self):
        if self.cleaned_data.get('age') == 'junior' and not self.cleaned_data.get('date_of_birth'):
            raise forms.ValidationError('Please provide age for Juniors.')

    class Meta:
        model = Beginner
        fields = ['name', 'contact_email', 'contact_number', 'age', 'date_of_birth', 'experience', 'notes']
