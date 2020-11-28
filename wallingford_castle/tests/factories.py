import datetime
import re

import factory
import factory.django
import factory.fuzzy
from faker import Faker

from ..models import Archer, User

fake = Faker()

EMAIL_RE = re.compile(r'(.+)(@.+)')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: re.sub(EMAIL_RE, r'\1{}\2', fake.email()).format(n))
    is_active = True


class ArcherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Archer

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('name')
    age = 'senior'
    date_of_birth = factory.fuzzy.FuzzyDate(
        datetime.date(1950, 1, 1),
        datetime.date(2000, 1, 1),
    )
