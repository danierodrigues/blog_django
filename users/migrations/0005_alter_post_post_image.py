# Generated by Django 4.0.1 on 2022-02-12 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_post_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
