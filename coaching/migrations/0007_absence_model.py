# Generated by Django 4.1 on 2022-09-23 21:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_alter_bookedslot_unique_together'),
        ('wallingford_castle', '0017_add_coaching_groups'),
        ('coaching', '0006_add_more_training_group_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupsession',
            name='booked_slot',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.bookedslot'),
        ),
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True, default='')),
                ('archer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallingford_castle.archer')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coaching.groupsession')),
            ],
            options={
                'unique_together': {('session', 'archer')},
            },
        ),
    ]
