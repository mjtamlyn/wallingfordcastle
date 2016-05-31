# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-31 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallingford_castle', '0002_membershipinterest_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='beginnerscourseinterest',
            name='contact_number',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='membershipinterest',
            name='contact_number',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]