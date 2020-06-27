import datetime

from django.test import TestCase

from dateutil.relativedelta import relativedelta

from ..models import Archer


class TestAgeGroup(TestCase):

    def test_senior(self):
        me = Archer(date_of_birth=datetime.date(1989, 1, 16))
        self.assertEqual(me.age_group, 'Senior')

    def test_junior_just_in_group(self):
        today = datetime.date.today()
        archer = Archer(date_of_birth=today - relativedelta(years=13, months=1))
        self.assertEqual(archer.age_group, 'U14')

    def test_junior_about_to_go_up(self):
        today = datetime.date.today()
        archer = Archer(date_of_birth=today - relativedelta(years=14, days=-10))
        self.assertTrue(archer.age_group.startswith('U14 (Moving up'))
