# Generated by Django 2.0.1 on 2018-04-19 12:11

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseSignup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('student_name', models.CharField(max_length=255)),
                ('student_date_of_birth', models.DateField()),
                ('experience', models.TextField(blank=True, default='')),
                ('notes', models.TextField(blank=True, default='')),
                ('gdpr_consent', models.BooleanField(default=False)),
                ('contact', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
    ]
