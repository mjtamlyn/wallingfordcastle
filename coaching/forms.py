from django import forms


class TrialContinueForm(forms.Form):
    name = forms.CharField(max_length=200)
    date_of_birth = forms.DateField()
    agb_number = forms.CharField(help_text='Archery GB membership is a requirement of club membership')
    contact_number = forms.CharField(
        max_length=20,
        help_text='Number for a parent or guardian to be used in case of emergency.',
    )
    address = forms.CharField(
        widget=forms.Textarea,
    )

    def __init__(self, trial, **kwargs):
        self.trial = trial
        initial = {
            'name': trial.archer.name,
            'date_of_birth': trial.archer.date_of_birth,
            'contact_number': trial.archer.contact_number,
        }
        initial.update(kwargs.get('initial', {}))
        kwargs['initial'] = initial
        super().__init__(**kwargs)

    def save(self):
        archer = self.trial.archer
        archer.agb_number = self.cleaned_data['agb_number']
        archer.name = self.cleaned_data['name']
        archer.date_of_birth = self.cleaned_data['date_of_birth']
        archer.contact_number = self.cleaned_data['contact_number']
        archer.address = self.cleaned_data['address']
        archer.save()

        member = archer.member_set.create(
            membership_type='full',
            coaching_subscription=self.trial.group.level.first().name in ['Junior Arrows', 'Novice'],
        )
        self.trial.group.participants.add(archer)
        return member
