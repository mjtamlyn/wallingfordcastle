# Generated by Django 2.1 on 2018-09-10 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallingford_castle', '0011_move_subscriptions_to_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archer',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='membershipinterest',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
