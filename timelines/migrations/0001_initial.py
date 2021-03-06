# Generated by Django 2.2.20 on 2022-01-03 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('url', models.CharField(max_length=100)),
                ('user_id', models.IntegerField()),
                ('username', models.CharField(max_length=50)),
                ('timestamp', models.CharField(max_length=100)),
                ('post_id', models.IntegerField()),
            ],
        ),
    ]
