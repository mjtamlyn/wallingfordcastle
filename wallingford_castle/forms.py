from django.contrib.auth.forms import SetPasswordForm

import floppyforms.__future__ as forms


from .models import MembershipInterest


class MembershipInterestForm(forms.ModelForm):
    def __init__(self, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(**kwargs)
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['date_of_birth'].required = True
        self.fields['agb_number'].label = 'ArcheryGB number'
        self.fields['agb_number'].help_text = 'If you have one'

    class Meta:
        model = MembershipInterest
        exclude = ['status']


class RegisterForm(SetPasswordForm):
    def save(self):
        self.user.is_active = True
        return super(RegisterForm, self).save()
