# Generated by Django 2.2.20 on 2022-01-04 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timelines', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_id',
        ),
    ]