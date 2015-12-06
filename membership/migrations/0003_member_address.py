# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0002_auto_20150930_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='address',
            field=models.TextField(default=''),
        ),
    ]
