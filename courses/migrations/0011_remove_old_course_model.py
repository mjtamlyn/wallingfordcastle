# Generated by Django 2.1.1 on 2018-09-18 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_add_course_coaches'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CourseSignup',
        ),
    ]
