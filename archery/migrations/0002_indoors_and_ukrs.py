# Generated by Django 5.0 on 2023-12-12 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='can_be_wrs',
            field=models.BooleanField(default=True),
        ),
    ]
