import datetime

from django.test import TestCase

from dateutil.relativedelta import relativedelta

from .factories import ArcherFactory, UserFactory


class TestFactoriesAndStr(TestCase):

    def test_user(self):
        user = UserFactory.create()
        str(user)

    def test_archer(self):
        archer = ArcherFactory.create()
        str(archer)


class TestAgeGroup(TestCase):

    def test_senior(self):
        me = ArcherFactory.build(date_of_birth=datetime.date(1989, 1, 16))
        self.assertEqual(me.age_group, 'Adult')

    def test_junior_just_in_group(self):
        today = datetime.date.today()
        archer = ArcherFactory.build(date_of_birth=today - relativedelta(years=13, months=1))
        self.assertEqual(archer.age_group, 'U14')
