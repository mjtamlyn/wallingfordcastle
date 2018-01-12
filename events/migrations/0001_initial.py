# Generated by Django 2.0.1 on 2018-01-11 17:50

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('membership', '0008_modernise_membership_types'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('guests', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=[], size=None)),
                ('date', models.DateTimeField()),
                ('duration', models.DurationField()),
            ],
        ),
        migrations.AddField(
            model_name='attendee',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event'),
        ),
        migrations.AddField(
            model_name='attendee',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.Member'),
        ),
        migrations.AlterUniqueTogether(
            name='attendee',
            unique_together={('member', 'event')},
        ),
    ]
