# Generated by Django 4.0.4 on 2022-09-11 12:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professional', '0002_auto_20220911_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professionreview',
            name='Review_Time',
            field=models.TimeField(default=datetime.datetime(2022, 9, 11, 17, 52, 32, 959911)),
        ),
        migrations.AlterField(
            model_name='professionreview_reply',
            name='Review_Reply_Time',
            field=models.TimeField(default=datetime.datetime(2022, 9, 11, 17, 52, 32, 959911)),
        ),
    ]
