# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallingford_castle', '0002_beginnerscourseinterest'),
    ]

    operations = [
        migrations.AddField(
            model_name='membershipinterest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processed', 'Processed'), ('beginners', 'Send to beginners course'), ('rejected', 'Rejected')], max_length=20, default='pending'),
        ),
        migrations.AlterField(
            model_name='membershipinterest',
            name='membership_type',
            field=models.CharField(choices=[('full', 'Full member'), ('student', 'Student member'), ('associate', 'Associate member')], max_length=20),
        ),
    ]
