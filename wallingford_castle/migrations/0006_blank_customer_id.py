# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-03 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallingford_castle', '0005_tournament_only_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='customer_id',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]