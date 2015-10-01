from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from custom_user.models import AbstractEmailUser
from templated_email import send_templated_mail
import stripe


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
        # TODO: Don't duplicate!
        with transaction.atomic():
            try:
                user = User.objects.get(email=self.contact_email)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=self.contact_email,
                    is_active=False,
                )
                user.send_welcome_email()
            member = user.members.create(
                name=self.name,
                age=self.age,
                date_of_birth=self.date_of_birth,
                agb_number=self.agb_number,
                membership_type=self.membership_type,
                interest=self,
            )
            if user.customer_id:
                customer = stripe.Customer.retrieve(user.customer_id)
                subscription = customer.subscriptions.create(plan=member.plan)
                member.subscription_id = subscription.id
                member.save()
                # TODO: Notify user they have a new subscription
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


class User(AbstractEmailUser):
    customer_id = models.CharField(max_length=20)

    def send_welcome_email(self, request=None):
        url = reverse('register', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': default_token_generator.make_token(self),
        })
        if request is not None:
            url = request.build_absolute_uri(url)
        send_templated_mail(
            template_name='welcome',
            from_email='hello@wallingfordcastle.co.uk',
            recipient_list=[self.email],
            context={
                'register_url': url,
            },
        )
