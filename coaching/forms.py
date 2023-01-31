from django import forms


class TrialContinueForm(forms.Form):
    name = forms.CharField(max_length=200)
    date_of_birth = forms.DateField()
    contact_number = forms.CharField(
        max_length=20,
        help_text='Number for a parent or guardian to be used in case of emergency.',
    )
    address = forms.CharField(
        widget=forms.Textarea,
        help_text='Joining the club includes joining Archery GB, the Governing body, who require a postal address.',
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
        archer.name = self.cleaned_data['name']
        archer.date_of_birth = self.cleaned_data['date_of_birth']
        archer.contact_number = self.cleaned_data['contact_number']
        archer.address = self.cleaned_data['address']
        archer.save()

        member = archer.member_set.create(
            membership_type='full',
            coaching_subscription=self.trial.group.level.first().name.startswith('Junior'),
        )
        self.trial.group.participants.add(archer)
        return member
