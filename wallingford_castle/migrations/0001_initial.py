# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('email', models.EmailField(unique=True, db_index=True, verbose_name='email address', max_length=255)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('customer_id', models.CharField(max_length=20)),
                ('groups', models.ManyToManyField(to='auth.Group', related_name='user_set', verbose_name='groups', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True)),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', related_name='user_set', verbose_name='user permissions', related_query_name='user', help_text='Specific permissions for this user.', blank=True)),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
        ),
        migrations.CreateModel(
            name='BeginnersCourseInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('contact_email', models.EmailField(max_length=254)),
                ('age', models.CharField(choices=[('junior', 'Junior'), ('senior', 'Senior')], max_length=20)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('experience', models.TextField(default='', blank=True)),
                ('notes', models.TextField(default='', blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MembershipInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('contact_email', models.EmailField(max_length=254)),
                ('age', models.CharField(choices=[('junior', 'Junior'), ('senior', 'Senior')], max_length=20)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('agb_number', models.CharField(max_length=10, default='', blank=True)),
                ('membership_type', models.CharField(choices=[('full', 'Full member'), ('student', 'Student member'), ('associate', 'Associate member')], max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processed', 'Processed'), ('beginners', 'Send to beginners course'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
