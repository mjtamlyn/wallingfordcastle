# Generated by Django 2.1 on 2018-09-15 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_remove_member_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='guests',
        ),
    ]