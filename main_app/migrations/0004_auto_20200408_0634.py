# Generated by Django 3.0.5 on 2020-04-08 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20200407_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='description',
            field=models.TextField(max_length=800),
        ),
    ]
