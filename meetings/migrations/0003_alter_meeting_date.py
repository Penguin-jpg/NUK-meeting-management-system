# Generated by Django 3.2.9 on 2021-11-28 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_remove_meeting_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateTimeField(),
        ),
    ]