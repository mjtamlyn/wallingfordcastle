# Generated by Django 2.0.1 on 2018-02-27 20:08

import django.contrib.postgres.fields.hstore
import django.contrib.postgres.operations
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0008_modernise_membership_types'),
        ('events', '0001_initial'),
    ]

    operations = [
        django.contrib.postgres.operations.CreateExtension('hstore'),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_answers', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
        ),
        migrations.CreateModel(
            name='BookingQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='bookable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bookingquestion',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event'),
        ),
        migrations.AddField(
            model_name='booking',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event'),
        ),
        migrations.AddField(
            model_name='booking',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.Member'),
        ),
        migrations.AlterUniqueTogether(
            name='bookingquestion',
            unique_together={('event', 'order')},
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('member', 'event')},
        ),
    ]
