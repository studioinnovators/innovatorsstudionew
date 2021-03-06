# Generated by Django 2.2.14 on 2021-08-31 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eduPlatform', '0065_auto_20210831_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='FullCourseTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150, null=True)),
                ('image', models.ImageField(upload_to='fullcourseteacherimages/')),
                ('phone_no', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('description', models.TextField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduPlatform.FullCourse')),
            ],
        ),
        migrations.CreateModel(
            name='MiniCourseTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150, null=True)),
                ('image', models.ImageField(upload_to='minicourseteacherimages/')),
                ('phone_no', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('description', models.TextField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduPlatform.MiniCourse')),
            ],
        ),
        migrations.CreateModel(
            name='PDPCourseTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150, null=True)),
                ('image', models.ImageField(upload_to='pdpcourseteacherimages/')),
                ('phone_no', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('description', models.TextField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduPlatform.PersonalDevelopmentCourse')),
            ],
        ),
        migrations.DeleteModel(
            name='TeacherProfile',
        ),
    ]
