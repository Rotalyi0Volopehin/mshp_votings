# Generated by Django 3.0.2 on 2020-01-19 10:09

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0014_auto_20200119_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voting',
            name='date_created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 1, 19, 13, 9, 11, 181548)),
        ),
        migrations.AlterField(
            model_name='voting',
            name='date_started',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 1, 19, 13, 9, 11, 181548)),
        ),
        migrations.AlterField(
            model_name='voting',
            name='date_stopped',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 1, 19, 13, 9, 11, 181548)),
        ),
        migrations.AlterField(
            model_name='votingset',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='votingset',
            name='date_created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 1, 19, 13, 9, 11, 181548)),
        ),
    ]