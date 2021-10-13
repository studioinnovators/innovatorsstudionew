# Generated by Django 2.2.14 on 2021-10-13 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eduPlatform', '0067_auto_20211013_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeCarousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='homecarousel/')),
                ('link', models.URLField()),
            ],
        ),
    ]