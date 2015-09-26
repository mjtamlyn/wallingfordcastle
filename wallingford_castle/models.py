from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils import timezone


AGE_CHOICES = (
    ('junior', 'Junior'),
    ('senior', 'Senior'),
)

MEMBERSHIP_CHOICES = (
    ('full', 'Full member'),
    ('student', 'Student member'),
    ('associate', 'Associate member'),
)

STATUS_PENDING = 'pending'
STATUS_PROCESSED = 'processed'
STATUS_BEGINNERS = 'beginners'
STATUS_REJECTED = 'rejected'
STATUS_CHOICES = (
    (STATUS_PENDING, 'Pending'),
    (STATUS_PROCESSED, 'Processed'),
    (STATUS_BEGINNERS, 'Send to beginners course'),
    (STATUS_REJECTED, 'Rejected'),
)


class MembershipInterest(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    age = models.CharField(max_length=20, choices=AGE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    agb_number = models.CharField(max_length=10, default='', blank=True)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def make_member(self, request=None):
        with transaction.atomic():
            try:
                user = User.objects.get(email=self.contact_email)
            except User.DoesNotExist:
                # TODO: Write a custom user model which has email auth and a
                # single name field
                user = User.objects.create(
                    email=self.contact_email,
                    username=self.contact_email,
                    is_active=False
                )
                # TODO send_invitation_email(user)
            user.members.create(
                name=self.name,
                age=self.age,
                date_of_birth=self.date_of_birth,
                agb_number=self.agb_number,
                membership_type=self.membership_type,
                interest=self,
            )
            self.status = STATUS_PROCESSED
            self.save()
            # TODO Slack notification with optional request.user


class BeginnersCourseInterest(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    age = models.CharField(max_length=20, choices=AGE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    experience = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='')

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
