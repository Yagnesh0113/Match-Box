# Generated by Django 4.0.4 on 2022-09-07 10:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professional', '0003_alter_professionreview_review_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professionreview',
            name='Review_Time',
            field=models.TimeField(default=datetime.datetime(2022, 9, 7, 16, 1, 14, 280906)),
        ),
        migrations.AlterField(
            model_name='professionreview_reply',
            name='Review_Reply_Time',
            field=models.TimeField(default=datetime.datetime(2022, 9, 7, 16, 1, 14, 280906)),
        ),
    ]
