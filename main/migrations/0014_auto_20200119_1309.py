# Generated by Django 3.0.2 on 2020-01-19 10:09

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0013_auto_20200119_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='votingset',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='votingset',
            name='date_created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 1, 19, 13, 9, 4, 126957)),
        ),
        migrations.AddField(
            model_name='votingset',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='votingset',
            name='title',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='voting',
            name='date_created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 1, 19, 13, 9, 4, 126957)),
        ),
        migrations.AlterField(
            model_name='voting',
            name='date_started',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 1, 19, 13, 9, 4, 126957)),
        ),
        migrations.AlterField(
            model_name='voting',
            name='date_stopped',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 1, 19, 13, 9, 4, 126957)),
        ),
    ]
