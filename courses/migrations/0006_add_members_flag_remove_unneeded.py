# Generated by Django 2.1 on 2018-09-02 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_add_course_interest_form'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendee',
            name='contact_number',
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='invoice_id',
        ),
        migrations.AddField(
            model_name='attendee',
            name='member',
            field=models.BooleanField(default=True),
        ),
    ]