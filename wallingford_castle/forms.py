import floppyforms.__future__ as forms

from .models import MembershipInterest, BeginnersCourseInterest


class MembershipInterestForm(forms.ModelForm):
    def __init__(self, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(**kwargs)
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['date_of_birth'].help_text = 'Juniors only'
        self.fields['agb_number'].label = 'ArcheryGB number'
        self.fields['agb_number'].help_text = 'If you have one'

    def clean(self):
        if self.cleaned_data.get('age') == 'junior' and not self.cleaned_data.get('date_of_birth'):
            raise forms.ValidationError('Please provide age for Juniors.')

    class Meta:
        model = MembershipInterest
        fields = '__all__'


class BeginnersCourseForm(forms.ModelForm):
    def __init__(self, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(**kwargs)
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['date_of_birth'].help_text = 'Juniors only'
        self.fields['experience'].label = 'Tell us about any archery you have done before'
        self.fields['experience'].help_text = 'No experience is necessary!'
        self.fields['notes'].label = 'Please tell us about any injuries or health problems, or anything else you think we should know'

    def clean(self):
        if self.cleaned_data.get('age') == 'junior' and not self.cleaned_data.get('date_of_birth'):
            raise forms.ValidationError('Please provide age for Juniors.')

    class Meta:
        model = BeginnersCourseInterest
        fields = '__all__'
