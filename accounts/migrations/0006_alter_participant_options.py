# Generated by Django 3.2.9 on 2021-11-26 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_profile_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={'permissions': [('request_for_modifying_meeting_minutes', '發出會議紀錄修改請求'), ('create_extempore_motion', '新增臨時動議'), ('mail_result', '寄出開會結果')]},
        ),
    ]
