from django.db import models


AGE_CHOICES = (
    ('junior', 'Junior'),
    ('senior', 'Senior'),
)

MEMBERSHIP_CHOICES = (
    ('full', 'Full member'),
    ('student', 'Student member'),
    ('associate', 'Associate member'),
)


class MembershipInterest(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    age = models.CharField(max_length=20, choices=AGE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    agb_number = models.CharField(max_length=10, default='', blank=True)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES)

    def __str__(self):
        return self.name


class BeginnersCourseInterest(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    age = models.CharField(max_length=20, choices=AGE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    experience = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name
