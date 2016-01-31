import floppyforms.__future__ as forms

from .models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'age', 'date_of_birth', 'address', 'contact_number', 'membership_type']

    def __init__(self, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(**kwargs)
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['date_of_birth'].help_text = 'Juniors only'

    def clean(self):
        if self.cleaned_data.get('age') == 'junior' and not self.cleaned_data.get('date_of_birth'):
            raise forms.ValidationError('Please provide age for Juniors.')
