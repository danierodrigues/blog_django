# Generated by Django 4.0.1 on 2022-01-23 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='pub_date',
        ),
        migrations.RemoveField(
            model_name='user',
            name='question_text',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
