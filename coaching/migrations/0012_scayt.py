# Generated by Django 5.0 on 2024-02-21 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coaching', '0011_alter_registration_wants_transport'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='scayt',
            field=models.BooleanField(default=False),
        ),
    ]