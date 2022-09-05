# Generated by Django 4.0.4 on 2022-09-05 08:18

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Account', '0003_remove_professionreview_reply_review_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessionReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Review', models.TextField()),
                ('Rate', models.IntegerField(default=0, validators=[django.core.validators.MaxLengthValidator(5), django.core.validators.MinLengthValidator(0)])),
                ('Review_Date', models.DateField(default=datetime.date(2022, 9, 5))),
                ('Review_Time', models.TimeField(default=datetime.datetime(2022, 9, 5, 13, 48, 50, 759772))),
                ('Profession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account.profession')),
                ('like', models.ManyToManyField(blank=True, null=True, to='Account.userprofile')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='Account.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Review_Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('Like', 'Like'), ('Unlike', 'Unlike')], default='Like', max_length=10)),
                ('profession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account.profession')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='ProfessionReview_Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Review_Reply', models.TextField()),
                ('Review_Reply_Date', models.DateField(default=datetime.date(2022, 9, 5))),
                ('Review_Reply_Time', models.TimeField(default=datetime.datetime(2022, 9, 5, 13, 48, 50, 759772))),
                ('Review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='professional.professionreview')),
                ('User_Profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account.userprofile')),
            ],
        ),
    ]
