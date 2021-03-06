# Generated by Django 2.2.1 on 2020-10-26 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_one_archer_only'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookedslot',
            name='group_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='bookedslot',
            name='is_group',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bookedslot',
            name='number_of_targets',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
