# Generated by Django 2.1 on 2018-09-13 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_fix_modified_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='group',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
