# Generated by Django 2.2.1 on 2020-09-27 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_add_description_fields_to_bookingtemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingtemplate',
            name='distance_required',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='bookingtemplate',
            name='multiple_archers_permitted',
            field=models.BooleanField(default=True),
        ),
    ]
