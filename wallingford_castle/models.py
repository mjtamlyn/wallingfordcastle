import collections
import datetime

from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.db import models, transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.http import urlsafe_base64_encode

import stripe
from custom_user.models import AbstractEmailUser
from dateutil.relativedelta import relativedelta
from templated_email import send_templated_mail

AGE_CHOICES = (
    ('junior', 'Junior'),
    ('senior', 'Senior'),
)

MEMBERSHIP_CHOICES = (
    ('full', 'Full member'),
    ('concession', 'Concession member'),
    ('associate', 'Associate member'),
    ('non-shooting', 'Non-shooting member'),
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
    coaching_subscription = models.BooleanField(default=False)

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def make_member(self, request=None):
        from membership.models import Member

        if self.member_set.exists():
            if request:
                messages.error(request, '%s has already been converted to a member.' % self.name)
            return
        with transaction.atomic():
            archer = None
            try:
                archer = Archer.objects.get(user__email=self.contact_email, name__iexact=self.name)
            except Archer.DoesNotExist:
                user, created = User.objects.get_or_create(email=self.contact_email, defaults={'is_active': False})
                if created:
                    user.send_new_user_email(request)
            else:
                user = archer.user
            if archer is None:
                archer = Archer.objects.create(
                    user=user,
                    name=self.name,
                    age=self.age,
                    date_of_birth=self.date_of_birth,
                    address=self.address,
                    contact_number=self.contact_number,
                    agb_number=self.agb_number,
                )
            elif not archer.address.strip():
                archer.address = self.address
                archer.save()
            member = Member.objects.create(
                archer=archer,
                membership_type=self.membership_type,
                coaching_subscription=self.coaching_subscription,
                interest=self,
            )
            self.status = STATUS_PROCESSED
            self.save()
            return member

    def send_to_beginners(self):
        from beginners.models import Beginner

        beginner = Beginner(
            name=self.name,
            contact_email=self.contact_email,
            contact_number=self.contact_number,
            age=self.age,
            date_of_birth=self.date_of_birth,
        )
        beginner.fee = beginner.get_2020_fee()
        beginner.save()
        self.status = STATUS_BEGINNERS
        self.save()


class User(AbstractEmailUser):
    customer_id = models.CharField(max_length=20, blank=True, default='')
    subscription_id = models.CharField(max_length=20, default='', blank=True)
    tournament_only = models.BooleanField(default=False)

    def generate_register_url(self, request=None):
        url = reverse('register', kwargs={
            'uidb64': urlsafe_base64_encode(str(self.pk).encode()),
            'token': default_token_generator.make_token(self),
        })
        if request is not None:
            url = request.build_absolute_uri(url)
        return url

    def send_new_user_email(self, request=None):
        url = self.generate_register_url(request)
        send_templated_mail(
            template_name='new_user',
            from_email='hello@wallingfordcastle.co.uk',
            recipient_list=[self.email],
            context={
                'register_url': url,
            },
        )

    def send_course_email(self, request=None, new_user=True):
        url = self.generate_register_url(request)
        send_templated_mail(
            template_name='course',
            from_email='hello@wallingfordcastle.co.uk',
            recipient_list=[self.email],
            context={
                'register_url': url if new_user else None,
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
            register_url = self.generate_register_url(request)
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

    def update_subscriptions(self):
        from membership.models import Member

        prices = collections.defaultdict(int)
        members = Member.objects.filter(archer__user=self, active=True)  # Just ones billed by this user
        for member in members:
            for price in member.prices:
                prices[price['id']] += 1

        if self.subscription_id:
            new_items = []
            subscription = stripe.Subscription.retrieve(self.subscription_id)
            for item in subscription['items']['data']:
                if item.price.id not in prices:
                    new_items.append({'id': item.id, 'deleted': True})
                else:
                    new_items.append({'id': item.id, 'quantity': prices.pop(item.price.id)})
            for price, quantity in prices.items():
                new_items.append({'price': price, 'quantity': quantity})
            subscription.items = new_items
            subscription.prorate = True
            subscription.save()
        else:
            new_items = []
            for price, quantity in prices.items():
                new_items.append({'price': price, 'quantity': quantity})
            customer = stripe.Customer.retrieve(self.customer_id)
            subscription = customer.subscriptions.create(items=new_items)
            self.subscription_id = subscription.id
            self.save()

    def add_invoice_item(self, amount, description):
        if not self.customer_id or not self.subscription_id:
            raise ValueError('User does not have a subscription')
        stripe.InvoiceItem.create(
            customer=self.customer_id,
            subscription=self.subscription_id,
            amount=amount,
            currency='gbp',
            description=description,
        )

    @cached_property
    def managed_members(self):
        from membership.models import Member
        return list(Member.objects.managed_by(self).select_related('archer').order_by('archer__name'))

    def manages_any(self, archers):
        return any(map(lambda m: m.archer in archers, self.managed_members))


class Archer(models.Model):
    """
    Represents any archer - members, non-members on courses, beginners,
    tournament visitors etc.
    """

    user = models.ForeignKey(User, related_name='archers', on_delete=models.CASCADE, blank=True, null=True)
    managing_users = models.ManyToManyField(User, related_name='managed_archers', blank=True)

    name = models.CharField(max_length=200)
    age = models.CharField(max_length=20, choices=AGE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    agb_number = models.CharField(max_length=10, default='', blank=True)
    address = models.TextField(blank=True, default='')
    contact_number = models.CharField(max_length=20, blank=True, default='')

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def age_group(self):
        if not self.date_of_birth:
            return None
        today = datetime.date.today()
        years = relativedelta(today, self.date_of_birth).years
        if years >= 25:
            return 'Senior'
        elif years < 8:
            group = 'U8'
        elif years < 10:
            group = 'U10'
        elif years < 12:
            group = 'U12'
        elif years < 14:
            group = 'U14'
        elif years < 16:
            group = 'U16'
        elif years < 18:
            group = 'U18'
        else:
            group = 'Senior (U25)'
        this_years_birthday = self.date_of_birth.replace(year=today.year)
        days_to_birthday = (this_years_birthday - today).days
        if days_to_birthday < 0:
            this_years_birthday += relativedelta(years=1)
            days_to_birthday = (this_years_birthday - today).days
        if days_to_birthday < 90 and years % 2:
            group += ' (Moving up on %s)' % this_years_birthday.strftime('%d/%m/%Y')
        return group
