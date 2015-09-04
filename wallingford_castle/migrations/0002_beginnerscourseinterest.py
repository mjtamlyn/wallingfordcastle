# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallingford_castle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeginnersCourseInterest',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('contact_email', models.EmailField(max_length=254)),
                ('age', models.CharField(choices=[('junior', 'Junior'), ('senior', 'Senior')], max_length=20)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('experience', models.TextField(default='', blank=True)),
                ('notes', models.TextField(default='', blank=True)),
            ],
        ),
    ]
