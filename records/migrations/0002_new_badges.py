# Generated by Django 2.1.1 on 2018-10-12 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_add_achievement_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='badge',
            field=models.CharField(choices=[('red-feather', 'Red Feather'), ('gold-feather', 'Gold Feather'), ('white-arrow', 'White Arrow'), ('black-arrow', 'Black Arrow'), ('blue-arrow', 'Blue Arrow'), ('white-half-portsmouth-150', 'White Half Portsmouth (150)'), ('black-half-portsmouth-175', 'Black Half Portsmouth (175)'), ('blue-half-portsmouth-200', 'Blue Half Portsmouth (200)'), ('red-half-portsmouth-225', 'Red Half Portsmouth (225)'), ('gold-half-portsmouth-250', 'Gold Half Portsmouth (250)'), ('purple-half-portsmouth-275', 'Purple Half Portsmouth (275)'), ('white-half-wa-18-150', 'White Half WA 18 (150)'), ('black-half-wa-18-175', 'Black Half WA 18 (175)'), ('blue-half-wa-18-200', 'Blue Half WA 18 (200)'), ('red-half-wa-18-225', 'Red Half WA 18 (225)'), ('gold-half-wa-18-250', 'Gold Half WA 18 (250)'), ('purple-half-wa-18-275', 'Purple Half WA 18 (275)')], max_length=31),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='badge_group',
            field=models.CharField(choices=[('wa-beginners', 'WA beginners'), ('half-portsmouth', 'Half Portsmouth'), ('half-wa-18', 'Half WA 18')], max_length=31),
        ),
    ]
