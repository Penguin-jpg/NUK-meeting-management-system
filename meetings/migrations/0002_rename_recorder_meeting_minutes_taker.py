# Generated by Django 3.2.9 on 2021-11-19 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting',
            old_name='recorder',
            new_name='minutes_taker',
        ),
    ]
