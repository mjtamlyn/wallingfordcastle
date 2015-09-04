import floppyforms.__future__ as forms

from .models import MembershipInterest


class MembershipInterestForm(forms.ModelForm):
    def __init__(self, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(**kwargs)
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['date_of_birth'].help_text = 'Juniors only'
        self.fields['agb_number'].label = 'ArcheryGB number'
        self.fields['agb_number'].help_text = 'If you have one'

    def clean(self):
        print(self.cleaned_data)
        if self.cleaned_data.get('age') == 'junior' and not self.cleaned_data.get('date_of_birth'):
            raise forms.ValidationError('Please provide age for Juniors.')

    class Meta:
        model = MembershipInterest
        fields = '__all__'
