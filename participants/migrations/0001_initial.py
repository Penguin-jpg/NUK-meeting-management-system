# Generated by Django 3.2.9 on 2021-11-19 01:55

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('account', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=20)),
                ('sex', models.IntegerField(choices=[(0, 'Female'), (1, 'Male')])),
                ('identity', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
            ],
        ),
    ]