# Generated by Django 2.1.1 on 2018-09-21 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_create_summer_archers'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='session_notes',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='session',
            name='session_plan',
            field=models.TextField(blank=True, default=''),
        ),
    ]