# Generated by Django 2.2.1 on 2020-06-27 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_add_attendee_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendeesession',
            name='attendee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_set', to='courses.Attendee'),
        ),
    ]