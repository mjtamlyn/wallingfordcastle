from django import forms

from membership.models import Member

from .models import Booking


class BookEventForm(forms.Form):
    def __init__(self, user, event, **kwargs):
        self.user = user
        self.event = event
        super().__init__(**kwargs)
        self.members = user.members.all()
        if len(self.members) > 1:
            self.fields['member'] = forms.ModelChoiceField(queryset=self.members)
        for question in event.bookingquestion_set.order_by('order'):
            self.fields['question_%s' % question.id] = forms.CharField(label=question.text)

    def clean_member(self):
        member = self.cleaned_data['member']
        if member.booking_set.filter(event=self.event).exists():
            raise forms.ValidationError('Member is already registered')
        return member

    def save(self):
        answers = {}
        for question in self.event.bookingquestion_set.order_by('order'):
            answers[question.text] = self.cleaned_data['question_%s' % question.id]
        if 'member' in self.cleaned_data:
            member = self.cleaned_data['member']
        else:
            member = self.members[0]
        return Booking.objects.create(
            event=self.event,
            member=member,
            response_answers=answers,
        )
