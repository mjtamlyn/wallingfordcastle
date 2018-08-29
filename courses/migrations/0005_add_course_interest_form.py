# Generated by Django 2.1 on 2018-08-29 20:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_expand_course_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_type', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=255)),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_number', models.CharField(blank=True, default='', max_length=20)),
                ('date_of_birth', models.DateField()),
                ('experience', models.TextField(blank=True, default='')),
                ('notes', models.TextField(blank=True, default='')),
                ('gdpr_consent', models.BooleanField(default=False)),
                ('contact', models.BooleanField(default=False)),
                ('communication_notes', models.TextField(blank=True, default='')),
                ('processed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
