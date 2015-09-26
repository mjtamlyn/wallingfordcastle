# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('age', models.CharField(choices=[('junior', 'Junior'), ('senior', 'Senior')], max_length=20)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('agb_number', models.CharField(blank=True, default='', max_length=10)),
                ('membership_type', models.CharField(choices=[('full', 'Full member'), ('student', 'Student member'), ('associate', 'Associate member')], max_length=20)),
                ('paid_until', models.DateField(null=True, blank=True)),
                ('user', models.ForeignKey(related_name='members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
