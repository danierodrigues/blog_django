# Generated by Django 4.0.1 on 2022-02-13 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_post_author_delete_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]