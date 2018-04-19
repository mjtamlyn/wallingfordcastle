from django import forms

from .models import CourseSignup


class CourseSignupForm(forms.ModelForm):
    email = forms.EmailField()
    student_name = forms.CharField()
    student_date_of_birth = forms.DateField()
    experience = forms.CharField(
        widget=forms.Textarea,
        label='Tell us about any archery you have done before',
        help_text='No experience is necessary!',
        required=False,
    )
    notes = forms.CharField(
        widget=forms.Textarea,
        label=(
            'Please tell us about any injuries or health problems, or anything '
            'else you think we should know'
        ),
        required=False,
    )
    gdpr_consent = forms.BooleanField(
        label='I consent that the information here provided will be shared with Wallingford Castle Archers and Didcot Girls School:',
    )
    contact = forms.BooleanField(
        label='Please contact me about future archery courses:',
        required=False,
    )

    class Meta:
        model = CourseSignup
        fields = ['email', 'student_name', 'student_date_of_birth', 'experience', 'notes', 'gdpr_consent', 'contact']
