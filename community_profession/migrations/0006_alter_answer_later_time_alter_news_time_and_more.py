# Generated by Django 4.0.4 on 2022-09-05 10:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community_profession', '0005_alter_answer_later_time_alter_news_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer_later',
            name='Time',
            field=models.TimeField(default=datetime.datetime(2022, 9, 5, 15, 42, 2, 809331)),
        ),
        migrations.AlterField(
            model_name='news',
            name='Time',
            field=models.TimeField(default=datetime.datetime(2022, 9, 5, 15, 42, 2, 808331)),
        ),
        migrations.AlterField(
            model_name='news_comment',
            name='Time',
            field=models.TimeField(default=datetime.datetime(2022, 9, 5, 15, 42, 2, 808331)),
        ),
        migrations.AlterField(
            model_name='news_comment_reply',
            name='Reply_Time',
            field=models.TimeField(default=datetime.datetime(2022, 9, 5, 15, 42, 2, 808331)),
        ),
        migrations.AlterField(
            model_name='user_question',
            name='Time',
            field=models.TimeField(default=datetime.datetime(2022, 9, 5, 15, 42, 2, 804334)),
        ),
    ]