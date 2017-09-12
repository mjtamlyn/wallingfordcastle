import datetime

from django.test import TestCase

from dateutil.relativedelta import relativedelta

from ..models import Member


class TestAgeGroup(TestCase):

    def test_senior(self):
        me = Member(date_of_birth=datetime.date(1989, 1, 16))
        self.assertEqual(me.age_group, 'Senior')

    def test_junior_just_in_group(self):
        today = datetime.date.today()
        member = Member(date_of_birth=today - relativedelta(years=13, months=1))
        self.assertEqual(member.age_group, 'U14')

    def test_junior_about_to_go_up(self):
        today = datetime.date.today()
        member = Member(date_of_birth=today - relativedelta(years=14, days=-10))
        self.assertTrue(member.age_group.startswith('U14 (Moving up'))
