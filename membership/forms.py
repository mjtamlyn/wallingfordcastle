from django import forms

from .models import MEMBERSHIP_CHOICES


class BaseMemberForm(forms.Form):
    name = forms.CharField(max_length=200)
    date_of_birth = forms.DateField(label='Date of Birth')
    address = forms.CharField(widget=forms.Textarea)
    contact_number = forms.CharField(max_length=20)
    medical_information = forms.CharField(widget=forms.Textarea)

    def __init__(self, instance, **kwargs):
        self.member = instance
        initial = kwargs.pop('initial', {})
        initial.update({
            'name': instance.archer.name,
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
        self.member.save()
        self.member.archer.save()
        return self.member


class SeniorMemberForm(BaseMemberForm):
    membership_type = forms.ChoiceField(choices=MEMBERSHIP_CHOICES)

    def save(self):
        self.member.membership_type = self.cleaned_data['membership_type']
        super().save()


class JuniorMemberForm(BaseMemberForm):
    primary_contact_name = forms.CharField(max_length=200)
    secondary_contact_name = forms.CharField(max_length=200)
    secondary_contact_number = forms.CharField(max_length=20)
    collection_consent = forms.BooleanField(required=False)
    collection_alternatives = forms.CharField(required=False, widget=forms.Textarea)
    photography_coaching = forms.BooleanField(required=False)
    photography_marketing = forms.BooleanField(required=False)

    def save(self):
        self.member.archer.primary_contact_name = self.cleaned_data['primary_contact_name']
        self.member.archer.secondary_contact_name = self.cleaned_data['secondary_contact_name']
        self.member.archer.secondary_contact_number = self.cleaned_data['secondary_contact_number']
        self.member.archer.collection_consent = self.cleaned_data['collection_consent']
        self.member.archer.collection_alternatives = self.cleaned_data['collection_alternatives']
        self.member.archer.photography_coaching = self.cleaned_data['photography_coaching']
        self.member.archer.photography_marketing = self.cleaned_data['photography_marketing']
        super().save()
