# Generated by Django 4.0.4 on 2022-09-09 09:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community_profession', '0044_answer_later_active_alter_news_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer_later',
            name='Active',
        ),
        migrations.AddField(
            model_name='user_question',
            name='Answer_later',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='news',
            name='Time',
            field=models.TimeField(default=datetime.datetime(2022, 9, 9, 15, 21, 4, 756498)),
        ),
        migrations.AlterField(
            model_name='news_comment_reply',
            name='Reply_Time',
            field=models.TimeField(default=datetime.datetime(2022, 9, 9, 15, 21, 4, 772126)),
        ),
    ]