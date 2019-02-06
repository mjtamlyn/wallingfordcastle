# Generated by Django 2.1 on 2018-09-15 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallingford_castle', '0014_build_events_from_sessions'),
        ('courses', '0009_build_events_from_sessions'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='coaches',
            field=models.ManyToManyField(blank=True, to='wallingford_castle.Archer'),
        ),
    ]