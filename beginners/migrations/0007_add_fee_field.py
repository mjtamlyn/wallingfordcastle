# Generated by Django 2.2.1 on 2020-07-16 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beginners', '0006_fix_modified_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='beginner',
            name='fee',
            field=models.IntegerField(default=80),
            preserve_default=False,
        ),
    ]