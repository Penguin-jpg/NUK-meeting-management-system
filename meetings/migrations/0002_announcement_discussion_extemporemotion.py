# Generated by Django 3.2.9 on 2021-12-17 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtemporeMotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposer', models.CharField(max_length=100, verbose_name='提案人')),
                ('content', models.CharField(max_length=500, verbose_name='內容')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.meeting', verbose_name='會議')),
            ],
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=25, verbose_name='案由')),
                ('description', models.CharField(max_length=500, verbose_name='說明')),
                ('resolution', models.CharField(max_length=150, verbose_name='決議')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.meeting', verbose_name='會議')),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500, verbose_name='內容')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.meeting', verbose_name='會議')),
            ],
        ),
    ]
