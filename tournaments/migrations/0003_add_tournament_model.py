# Generated by Django 2.0.1 on 2018-03-15 19:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0002_blank_customer_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('date', models.DateField()),
                ('rounds', models.TextField()),
                ('event_format', models.TextField()),
                ('judges', models.TextField()),
                ('awards', models.TextField()),
                ('tournament_organiser', models.CharField(max_length=200)),
                ('tournament_organiser_email', models.EmailField(max_length=254)),
                ('dress', models.TextField()),
                ('drug_testing', models.TextField()),
                ('timing', models.TextField()),
                ('venue_description', models.TextField()),
                ('venue_google_search', models.CharField(max_length=200)),
                ('refreshments', models.TextField()),
                ('camping', models.TextField()),
                ('entry_information', models.TextField()),
                ('entry_fee', models.IntegerField()),
                ('entries_open', models.DateTimeField()),
                ('entries_close', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='tournament',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tournaments.Tournament'),
        ),
    ]
