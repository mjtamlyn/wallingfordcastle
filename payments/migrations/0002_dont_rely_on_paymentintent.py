# Generated by Django 5.0 on 2023-12-15 12:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel('paymentintent', 'checkout'),
        migrations.RenameField('lineitemintent', 'payment_intent', 'checkout'),
    ]