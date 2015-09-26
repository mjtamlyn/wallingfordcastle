# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wallingford_castle', '0004_auto_20150926_2126'),
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='member',
            name='interest',
            field=models.ForeignKey(to='wallingford_castle.MembershipInterest', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='modified',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=False,
        ),
    ]
