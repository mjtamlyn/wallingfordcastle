# Generated by Django 2.0.1 on 2018-01-05 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallingford_castle', '0006_blank_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membershipinterest',
            name='membership_type',
            field=models.CharField(choices=[('full', 'Full member'), ('concession', 'Concession member'), ('associate', 'Associate member'), ('non-shooting', 'Non-shooting member')], max_length=20),
        ),
    ]
