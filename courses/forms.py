import datetime

from django import forms

from membership.models import Member
from .models import Attendee, CourseSignup, Interest, Summer2018Signup


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


class Summer2018SignupForm(forms.ModelForm):
    contact_name = forms.CharField()
    email = forms.EmailField(label='Contact email')
    contact_number = forms.CharField()
    student_name = forms.CharField()
    student_date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type' :'date'}))
    group = forms.ChoiceField(choices=(
        ('', '---------'),
        ('6-12 beginners', '6-12 beginners'),
        ('6-12 intermediates', '6-12 intermediates'),
        ('12-18 beginners', '12-18 beginners'),
        ('12-18 intermediates', '12-18 intermediates'),
    ))
    dates = forms.MultipleChoiceField(choices=(
        ('2018-07-26', 'Thursday 26th July'),
        ('2018-07-31', 'Tuesday 31st July'),
        ('2018-08-02', 'Thursday 2nd August'),
        ('2018-08-07', 'Tuesday 7th August'),
        ('2018-08-09', 'Thursday 9th August'),
        ('2018-08-14', 'Tuesday 14th August'),
        ('2018-08-16', 'Thursday 16th August'),
        ('2018-08-21', 'Tuesday 21st August'),
        ('2018-08-23', 'Thursday 23rd August'),
        ('2018-08-28', 'Tuesday 28th August'),
        ('2018-08-30', 'Thursday 30th August'),
        ('2018-09-04', 'Tuesday 4th September'),
    ), widget=forms.CheckboxSelectMultiple)
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
            label='I consent that the information here provided will be stored by Wallingford Castle Archers:'
    )
    contact_consent = forms.BooleanField(
        label='Please contact me about future archery courses:',
        required=False,
    )

    class Meta:
        model = Summer2018Signup
        fields = [
            'contact_name', 'email', 'contact_number', 'student_name',
            'student_date_of_birth', 'group', 'dates', 'experience', 'notes',
            'gdpr_consent', 'contact_consent',
        ]


class MinisInterestForm(forms.ModelForm):
    name = forms.CharField(label='Archer name')
    contact_email = forms.EmailField()
    contact_number = forms.CharField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type' :'date'}))
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
            label='I consent that the information here provided will be stored by Wallingford Castle Archers:'
    )
    contact = forms.BooleanField(
        label='Please contact me about future archery courses:',
        required=False,
    )

    class Meta:
        model = Interest
        fields = [
            'contact_email', 'contact_number', 'name', 'date_of_birth',
            'experience', 'notes', 'gdpr_consent', 'contact',
        ]

    def save(self):
        self.instance.course_type = 'minis'
        return super().save()


class MembersBookCourseForm(forms.Form):
    def __init__(self, user, course, **kwargs):
        self.user = user
        self.course = course
        super().__init__(**kwargs)
        self.members = Member.objects.managed_by(user)
        self.fields['member'] = forms.ModelChoiceField(queryset=self.members)
        self.fields['acknowledgement' ] = forms.BooleanField(
            label='I understand that the cost of the course will be added to the next membership payment',
            required=True,
        )

    def clean_member(self):
        member = self.cleaned_data['member']
        if member.archer.attendee_set.filter(course=self.course).exists():
            raise forms.ValidationError('%s is already registered' % member.archer)
        return member

    def save(self):
        answers = {}
        if 'member' in self.cleaned_data:
            member = self.cleaned_data['member']
        member.archer.user.add_invoice_item(
            amount=self.course.members_price * 100,
            description='%s for %s' % (self.course, member),
        )
        return Attendee.objects.create(
            course=self.course,
            archer=member.archer,
            paid=True,
        )
