# Generated by Django 4.1 on 2023-02-17 09:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_alter_bookedslot_unique_together'),
        ('tournaments', '0009_series_entries'),
        ('wallingford_castle', '0017_add_coaching_groups'),
        ('coaching', '0007_absence_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArcherSeason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_classification', models.CharField(choices=[('A3', 'Archer 3rd class'), ('A2', 'Archer 2nd class'), ('A1', 'Archer 1st class'), ('B3', 'Bowman 3rd class'), ('B2', 'Bowman 2nd class'), ('B1', 'Bowman 1st class'), ('MB', 'Master Bowman'), ('GMB', 'Grand Master Bowman'), ('EMB', 'Elite Master Bowman')], max_length=3)),
                ('personalised_target_comments', models.TextField(blank=True, default='')),
                ('archer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallingford_castle.archer')),
            ],
        ),
        migrations.CreateModel(
            name='CompetitiveTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wallingford_castle.season')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('event_format', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('venue', models.CharField(max_length=255)),
                ('venue_post_code', models.CharField(max_length=20)),
                ('age_groups', models.CharField(max_length=100)),
                ('club_trip', models.BooleanField(default=False)),
                ('entry_link', models.URLField(blank=True, null=True)),
                ('event_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.event')),
                ('tournament_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournaments.tournament')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coaching.competitivetrack')),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('definite', 'Yes, I am definitely attending'), ('booked', 'Yes, I am booked in'), ('maybe', 'I might be attending'), ('no', 'I will not be attending')], max_length=20)),
                ('wants_transport', models.CharField(choices=[('required', 'I can only attend if transport is offered'), ('interested', 'Transport for archer would be helpful but we could make our own way there'), ('plus-parent', 'Transport for archer and a parent would be helpful but we could make our own way there'), ('own-way', 'We will make our own way there')], max_length=20)),
                ('archer_season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coaching.archerseason')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coaching.event')),
            ],
        ),
        migrations.CreateModel(
            name='ArcherTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommended_events_comments', models.TextField(blank=True, default='')),
                ('archer_season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coaching.archerseason')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coaching.competitivetrack')),
            ],
        ),
        migrations.AddField(
            model_name='archerseason',
            name='events',
            field=models.ManyToManyField(through='coaching.Registration', to='coaching.event'),
        ),
        migrations.AddField(
            model_name='archerseason',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wallingford_castle.season'),
        ),
        migrations.AddField(
            model_name='archerseason',
            name='tracks',
            field=models.ManyToManyField(through='coaching.ArcherTrack', to='coaching.competitivetrack'),
        ),
    ]
