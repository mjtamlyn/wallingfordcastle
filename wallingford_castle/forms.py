from django.contrib.auth.forms import SetPasswordForm

import floppyforms.__future__ as forms

from wallingford_castle.models import User

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



class CompliantPasswordInput(forms.PasswordInput):
    def render(self, name, value, attrs=None, renderer=None):
        return super().render(name, value, attrs=None)



class DirectRegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=CompliantPasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                code='duplicate',
                message='A user with that email address already exists',
            )
        return email

    def save(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(email=email, password=password)
        return user
