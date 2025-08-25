from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.template import loader

from wallingford_castle.models import User

from .mail import api_client, domain
from .models import MembershipInterest


class MembershipInterestForm(forms.ModelForm):
    def __init__(self, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(**kwargs)
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['date_of_birth'].required = True
        self.fields['agb_number'].label = 'Archery GB number'
        self.fields['agb_number'].help_text = 'Archery GB membership is required'
        self.fields['date_of_birth'].required = True

    class Meta:
        model = MembershipInterest
        exclude = ['status', 'coaching_subscription']


class ClientPasswordResetForm(PasswordResetForm):
    def send_mail(
            self, subject_template_name, email_template_name, context,
            from_email, to_email, html_email_template_name=None):

        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        message_data = {
            'from': from_email or 'Wallingford Castle Archers <hello@wallingfordcastle.co.uk>',
            'to': to_email,
            'subject': subject,
            'text': body,
        }
        if api_client:
            api_client.messages.create(data=message_data, domain=domain)
        else:
            print(message_data)


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
