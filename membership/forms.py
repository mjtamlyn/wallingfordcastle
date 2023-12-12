from django import forms

from wallingford_castle.models import AGE_CHOICES

from .models import MEMBERSHIP_CHOICES


class MemberForm(forms.Form):
    name = forms.CharField(max_length=255)
    age = forms.ChoiceField(choices=AGE_CHOICES)
    date_of_birth = forms.DateField(label='Date of Birth')
    address = forms.CharField(widget=forms.Textarea)
    contact_number = forms.CharField(max_length=255)
    membership_type = forms.ChoiceField(choices=MEMBERSHIP_CHOICES)

    def __init__(self, instance, **kwargs):
        self.member = instance
        initial = kwargs.pop('initial', {})
        initial.update({
            'name': instance.archer.name,
            'age': instance.archer.age,
            'date_of_birth': instance.archer.date_of_birth,
            'address': instance.archer.address,
            'contact_number': instance.archer.contact_number,
            'membership_type': instance.membership_type,
        })
        kwargs.setdefault('label_suffix', '')
        super().__init__(initial=initial, **kwargs)

    def save(self):
        self.member.archer.name = self.cleaned_data['name']
        self.member.archer.age = self.cleaned_data['age']
        self.member.archer.date_of_birth = self.cleaned_data['date_of_birth']
        self.member.archer.address = self.cleaned_data['address']
        self.member.archer.contact_number = self.cleaned_data['contact_number']
        self.member.membership_type = self.cleaned_data['membership_type']
        self.member.save()
        self.member.archer.save()
        return self.member
