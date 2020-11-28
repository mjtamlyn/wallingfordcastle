# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('age', models.CharField(choices=[('junior', 'Junior'), ('senior', 'Senior')], max_length=20)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('agb_number', models.CharField(max_length=10, default='', blank=True)),
                ('membership_type', models.CharField(choices=[('full', 'Full member'), ('student', 'Student member'), ('associate', 'Associate member')], max_length=20)),
                ('paid_until', models.DateField(null=True, blank=True)),
                ('subscription_id', models.CharField(editable=False, max_length=20, default='', blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
