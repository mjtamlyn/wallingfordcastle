# Generated by Django 2.2.1 on 2020-06-27 11:24

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_add_booked_slots'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_times', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), size=None)),
                ('targets', models.PositiveIntegerField()),
                ('booking_duration', models.DurationField()),
            ],
        ),
    ]
