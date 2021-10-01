import datetime

from django import forms
from django.conf import settings
from django.contrib.postgres.forms import JSONField

from membership.models import Member

from .models import BookedSlot, Booking


class BookEventForm(forms.Form):
    def __init__(self, user, event, **kwargs):
        self.user = user
        self.event = event
        super().__init__(**kwargs)
        self.members = Member.objects.managed_by(user)
        if len(self.members) > 1:
            self.fields['member'] = forms.ModelChoiceField(queryset=self.members)
        for question in event.bookingquestion_set.order_by('order'):
            self.fields['question_%s' % question.id] = forms.CharField(label=question.text)

    def clean_member(self):
        member = self.cleaned_data['member']
        if member.archer.booking_set.filter(event=self.event).exists():
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
            archer=member.archer,
            response_answers=answers,
        )


class BookSlotForm(forms.Form):
    date = forms.DateField()
    time = forms.TimeField()
    target = forms.IntegerField()
    face = forms.CharField(required=False)
    distance = forms.CharField(required=False)
    archers = JSONField()

    def __init__(self, user, **kwargs):
        self.user = user
        super().__init__(**kwargs)

    def clean_archers(self):
        archers = self.cleaned_data.get('archers')
        members = Member.objects.managed_by(self.user)
        return members.filter(id__in=archers)

    def clean(self):
        data = self.cleaned_data
        # TODO: check distance properly, will require looking up the template
        return data

    def save(self):
        data = self.cleaned_data
        start = datetime.datetime.combine(data['date'], data['time'])
        start = settings.TZ.localize(start)
        duration = datetime.timedelta(minutes=90)  # TODO: submit this somehow?
        target = data['target']
        distance = data['distance']
        archers = data['archers']
        face = None
        if data['face']:
            face = {'A': 1, 'B': 2}[data['face']]
        slot = BookedSlot.objects.create(
            start=start,
            duration=duration,
            target=target,
            face=face,
            distance=distance,
        )
        slot.archers.set(a.archer for a in archers)
        return slot


class CancelSlotForm(forms.Form):
    date = forms.DateField()
    time = forms.TimeField()
    target = forms.IntegerField()
    face = forms.CharField(required=False)

    def __init__(self, user, **kwargs):
        self.user = user
        super().__init__(**kwargs)

    def clean(self):
        data = self.cleaned_data
        start = datetime.datetime.combine(data['date'], data['time'])
        start = settings.TZ.localize(start)
        face = None
        if data['face']:
            face = {'A': 1, 'B': 2}[data['face']]
        slot = BookedSlot.objects.get(
            start=start,
            target=data['target'],
            face=face,
        )
        # TODO: check I have the right to delete this
        data['slot'] = slot
        return data

    def save(self):
        self.cleaned_data['slot'].delete()
