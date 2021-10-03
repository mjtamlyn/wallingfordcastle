# Generated by Django 3.2 on 2021-10-03 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0001_add_venue_model'),
        ('events', '0019_multiface_bookings'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingtemplate',
            name='venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='venues.venue'),
        ),
    ]
