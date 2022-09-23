# Generated by Django 4.1 on 2022-09-23 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0001_add_venue_model'),
        ('events', '0023_populate_slot_venue'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookedslot',
            unique_together={('start', 'target', 'face', 'venue')},
        ),
    ]
