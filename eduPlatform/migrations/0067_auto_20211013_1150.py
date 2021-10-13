# Generated by Django 2.2.14 on 2021-10-13 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eduPlatform', '0066_auto_20210831_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fullcourse',
            name='inoffice',
        ),
        migrations.RemoveField(
            model_name='fullcourse',
            name='live_one_to_one',
        ),
        migrations.RemoveField(
            model_name='minicourse',
            name='inoffice',
        ),
        migrations.RemoveField(
            model_name='minicourse',
            name='live_one_to_one',
        ),
        migrations.RemoveField(
            model_name='personaldevelopmentcourse',
            name='inoffice',
        ),
        migrations.RemoveField(
            model_name='personaldevelopmentcourse',
            name='live_one_to_one',
        ),
        migrations.AddField(
            model_name='fullcourse',
            name='online',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='minicourse',
            name='online',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personaldevelopmentcourse',
            name='online',
            field=models.BooleanField(default=False),
        ),
    ]