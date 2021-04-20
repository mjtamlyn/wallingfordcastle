# Generated by Django 3.1.7 on 2021-04-14 12:37

from django.conf import settings
from django.db import migrations


def migrate_times(apps, editor):
    Event = apps.get_model('events', 'Event')
    for event in Event.objects.all():
        event.date = settings.TZ.localize(event.date.replace(tzinfo=None))
        event.save(update_fields=['date'])

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_archers_not_required'),
    ]

    operations = [
        migrations.RunPython(migrate_times, migrations.RunPython.noop),
    ]