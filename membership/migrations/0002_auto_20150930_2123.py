# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
        ('wallingford_castle', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='interest',
            field=models.ForeignKey(null=True, blank=True, to='wallingford_castle.MembershipInterest', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(related_name='members', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
    ]
