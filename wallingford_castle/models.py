from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
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
    contact_number = models.CharField(max_length=20, blank=True, default='')
    age = models.CharField(max_length=20, choices=AGE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(default='')
    agb_number = models.CharField(max_length=10, default='', blank=True)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def make_member(self, request=None):
        if self.member_set.exists():
            if request:
                messages.error(request, '%s has already been converted to a member.' % self.name)
            return
        with transaction.atomic():
            user, created = User.objects.get_or_create(email=self.contact_email, defaults={'is_active': False})
            if created:
                user.send_new_user_email(request)
            member = user.members.create(
                name=self.name,
                age=self.age,
                date_of_birth=self.date_of_birth,
                address=self.address,
                contact_number=self.contact_number,
                agb_number=self.agb_number,
                membership_type=self.membership_type,
                interest=self,
            )
            if user.customer_id:
                customer = stripe.Customer.retrieve(user.customer_id)
                subscription = customer.subscriptions.create(plan=member.plan)
                member.subscription_id = subscription.id
                member.save()
                user.send_welcome_email()
            self.status = STATUS_PROCESSED
            self.save()

    def send_to_beginners(self):
        from beginners.models import Beginner

        Beginner.objects.create(
            name=self.name,
            contact_email=self.contact_email,
            contact_number=self.contact_number,
            age=self.age,
            date_of_birth=self.date_of_birth,
        )
        self.status = STATUS_BEGINNERS
        self.save()


class User(AbstractEmailUser):
    customer_id = models.CharField(max_length=20)
    tournament_only = models.BooleanField(default=False)

    def send_new_user_email(self, request=None):
        url = reverse('register', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': default_token_generator.make_token(self),
        })
        if request is not None:
            url = request.build_absolute_uri(url)
        send_templated_mail(
            template_name='new_user',
            from_email='hello@wallingfordcastle.co.uk',
            recipient_list=[self.email],
            context={
                'register_url': url,
            },
        )

    def send_welcome_email(self, request=None):
        send_templated_mail(
            template_name='welcome',
            from_email='hello@wallingfordcastle.co.uk',
            recipient_list=[self.email],
            context={},
        )

    def send_beginners_course_email(self, request, beginners, course, created):
        if not self.is_active:
            register_url = reverse('register', kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(self.pk)),
                'token': default_token_generator.make_token(self),
            })
            register_url = request.build_absolute_uri(register_url)
        else:
            register_url = None
        send_templated_mail(
            template_name='beginners_course',
            from_email='hello@wallingfordcastle.co.uk',
            recipient_list=[self.email],
            context={
                'beginners': beginners,
                'course': course,
                'register_url': register_url,
                'overview_url': request.build_absolute_uri(reverse('membership:overview'))
            }
        )
