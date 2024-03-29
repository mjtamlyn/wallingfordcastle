# Generated by Django 3.2 on 2021-04-20 12:47

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archery', '__first__'),
        ('tournaments', '0005_indoor_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='round',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='archery.round'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='bowstyles',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('recurve', 'Recurve'), ('compound', 'Compound'), ('barebow', 'Barebow'), ('longbow', 'Longbow'), ('flatbow', 'American Flatbow')], max_length=30), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tournament',
            name='has_wrs',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='bowstyle',
            field=models.CharField(choices=[('recurve', 'Recurve'), ('compound', 'Compound'), ('barebow', 'Barebow'), ('longbow', 'Longbow'), ('flatbow', 'American Flatbow')], max_length=50),
        ),
        migrations.RenameField(
            model_name='tournament',
            old_name='rounds',
            new_name='old_rounds',
        ),
        migrations.AddField(
            model_name='tournament',
            name='rounds',
            field=models.ManyToManyField(to='archery.Round'),
        ),
    ]
