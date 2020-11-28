# Generated by Django 2.0.1 on 2018-08-13 10:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallingford_castle', '0010_refine_member_archer_link'),
        ('membership', '0008_modernise_membership_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='archer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wallingford_castle.Archer'),
        ),
    ]
