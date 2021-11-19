# Generated by Django 3.2.9 on 2021-11-19 02:30

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0003_expert'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assistant',
            fields=[
                ('participant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='participants.participant')),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='TW')),
            ],
            bases=('participants.participant',),
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('participant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='participants.participant')),
                ('title', models.CharField(max_length=20)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='TW')),
            ],
            bases=('participants.participant',),
        ),
        migrations.CreateModel(
            name='StudentRepresentative',
            fields=[
                ('participant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='participants.participant')),
                ('student_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('school_system', models.CharField(max_length=10)),
                ('grade', models.CharField(max_length=10)),
            ],
            bases=('participants.participant',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('participant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='participants.participant')),
                ('school', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=20)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='TW')),
                ('address', models.CharField(max_length=100)),
                ('bank_account', models.CharField(max_length=14)),
            ],
            bases=('participants.participant',),
        ),
        migrations.RenameField(
            model_name='expert',
            old_name='job_title',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='participant',
            name='account',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
