# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallingford_castle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='membershipinterest',
            name='address',
            field=models.TextField(default=''),
        ),
    ]
