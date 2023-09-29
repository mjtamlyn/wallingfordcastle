# Generated by Django 4.1.7 on 2023-09-29 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0014_coaching_subscription_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='level',
        ),
        migrations.AddField(
            model_name='member',
            name='coaching_conversion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='coaching_performance',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='gym_supplement',
            field=models.BooleanField(default=False),
        ),
    ]
