# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('contact_email', models.EmailField(max_length=254)),
                ('age', models.CharField(choices=[('junior', 'Junior'), ('senior', 'Senior')], max_length=20)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('agb_number', models.CharField(default='', blank=True, max_length=10)),
                ('membership_type', models.CharField(choices=[('full', 'Full member'), ('associate', 'Associate member')], max_length=20)),
            ],
        ),
    ]
