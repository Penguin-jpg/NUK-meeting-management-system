# Generated by Django 3.2.9 on 2021-12-23 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='meeting',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='announcements', to='meetings.meeting', verbose_name='會議'),
        ),
        migrations.AlterField(
            model_name='appendix',
            name='meeting',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appendices', to='meetings.meeting', verbose_name='會議'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='meeting',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendance', to='meetings.meeting', verbose_name='會議'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='attendance_records', to=settings.AUTH_USER_MODEL, verbose_name='與會人員'),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='meeting',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='discussions', to='meetings.meeting', verbose_name='會議'),
        ),
        migrations.AlterField(
            model_name='extemporemotion',
            name='meeting',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='extempore_motions', to='meetings.meeting', verbose_name='會議'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='chairman',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='host_meeting', to=settings.AUTH_USER_MODEL, verbose_name='主席'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='minutes_taker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='take_minutes_meeting', to=settings.AUTH_USER_MODEL, verbose_name='記錄人員'),
        ),
    ]
