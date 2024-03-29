from django import forms
from django.db import transaction

from membership.models import Member
from wallingford_castle.models import Archer

from .models import Attendee, Interest


class CourseInterestForm(forms.ModelForm):
    name = forms.CharField(label='Archer name')
    contact_email = forms.EmailField()
    contact_number = forms.CharField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
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

    def __init__(self, **kwargs):
        self.course_type = kwargs.pop('course_type', 'unknown')
        super().__init__(**kwargs)

    def save(self):
        self.instance.course_type = self.course_type
        return super().save()


class MembersBookCourseForm(forms.Form):
    def __init__(self, user, course, **kwargs):
        self.user = user
        self.course = course
        super().__init__(**kwargs)
        self.members = Member.objects.managed_by(user)
        self.fields['member'] = forms.ModelChoiceField(queryset=self.members)
        self.fields['acknowledgement'] = forms.BooleanField(
            label='I understand that the cost of the course will be added to the next membership payment',
            required=True,
        )

    def clean_member(self):
        member = self.cleaned_data['member']
        if member.archer.attendee_set.filter(course=self.course).exists():
            raise forms.ValidationError('%s is already registered' % member.archer)
        return member

    def save(self):
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


class NonMembersBookCourseForm(forms.Form):
    def __init__(self, user, course, **kwargs):
        self.user = user
        self.course = course
        super().__init__(**kwargs)
        self.archers = Archer.objects.filter(user=user)
        self.fields['archer'] = forms.ModelChoiceField(queryset=self.archers)
        if len(self.archers) == 1:
            self.fields['archer'].initial = self.archers[0].pk
            self.fields['archer'].disabled = True

    def clean_archer(self):
        archer = self.cleaned_data['archer']
        if archer.attendee_set.filter(course=self.course).exists():
            raise forms.ValidationError('%s is already registered' % archer)
        return archer

    def save(self):
        return Attendee.objects.create(
            course=self.course,
            archer=self.cleaned_data['archer'],
            paid=False,
            member=False,
        )


class SessionBookingForm(forms.Form):
    class CancellationException(Exception):
        pass

    def __init__(self, course, booked=None, **kwargs):
        self.course = course
        super().__init__(**kwargs)
        if booked:
            booked_dict = {session.session_id: session for session in booked}
        else:
            booked_dict = {}
        for session in course.session_set.order_by('start_time'):
            self.fields['session_%s' % session.pk] = forms.BooleanField(
                label=session.label,
                label_suffix='',
                required=False,
                initial=session.pk in booked_dict,
            )

    def save(self, archer_id):
        archer = Archer.objects.get(pk=archer_id)
        try:
            attendee = archer.attendee_set.get(course=self.course)
        except Attendee.DoesNotExist:
            is_member = archer.member_set.filter(active=True).exists()
            attendee = Attendee.objects.create(archer=archer, course=self.course, member=is_member)
        sessions_booked = attendee.session_set.all()
        session_dict = {session.session_id: session for session in sessions_booked}
        with transaction.atomic():
            for session in self.course.session_set.all():
                if session.pk in session_dict:
                    if not self.cleaned_data['session_%s' % session.pk]:
                        if session_dict[session.pk].paid:
                            raise self.CancellationException
                        else:
                            session_dict[session.pk].delete()
                else:
                    if self.cleaned_data['session_%s' % session.pk]:
                        attendee.session_set.create(session=session)
