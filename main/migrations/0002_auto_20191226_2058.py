# Generated by Django 3.0.1 on 2019-12-26 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voting',
            old_name='aut_hor',
            new_name='author',
        ),
    ]
