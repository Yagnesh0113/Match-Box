# Generated by Django 4.0.4 on 2022-11-10 12:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community_profession', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='Date',
            field=models.DateField(default=datetime.date(2022, 11, 10)),
        ),
        migrations.AlterField(
            model_name='news',
            name='Time',
            field=models.TimeField(default=datetime.datetime(2022, 11, 10, 18, 25, 57, 869926)),
        ),
        migrations.AlterField(
            model_name='news_comment_reply',
            name='Reply_Time',
            field=models.TimeField(default=datetime.datetime(2022, 11, 10, 18, 25, 57, 872918)),
        ),
    ]