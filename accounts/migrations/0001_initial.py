# Generated by Django 3.2.9 on 2021-12-11 05:29

import accounts.models
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='電子信箱')),
                ('identity', models.IntegerField(choices=[(0, '業界專家'), (1, '學生代表'), (2, '校外老師'), (3, '系助理'), (4, '系上老師')], default=0, verbose_name='身分')),
                ('sex', models.IntegerField(choices=[(0, '女性'), (1, '男性'), (2, '其他')], default=2, verbose_name='性別')),
                ('phone', models.CharField(max_length=20, verbose_name='連絡電話')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': [('request_for_modifying_meeting_minutes', '發出會議紀錄修改請求'), ('create_extempore_motion', '新增臨時動議'), ('mail_result', '寄出開會結果')],
            },
            managers=[
                ('objects', accounts.models.ParticipantManager()),
            ],
        ),
        migrations.CreateModel(
            name='TeacherInfo',
            fields=[
                ('info_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.info')),
                ('telephone', models.CharField(max_length=20, verbose_name='辦公室電話')),
                ('title', models.CharField(max_length=20, verbose_name='職稱')),
                ('address', models.CharField(max_length=100, verbose_name='聯絡地址')),
                ('bank_account', models.CharField(max_length=14, verbose_name='銀行(郵局)帳號')),
                ('school', models.CharField(max_length=50, verbose_name='任職學校')),
                ('department', models.CharField(max_length=20, verbose_name='系所')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_info', to=settings.AUTH_USER_MODEL, verbose_name='使用者')),
            ],
            bases=('accounts.info',),
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('info_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.info')),
                ('student_id', models.CharField(max_length=15, verbose_name='學號')),
                ('school_system', models.CharField(max_length=10, verbose_name='學制')),
                ('grade', models.CharField(max_length=10, verbose_name='年級')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_info', to=settings.AUTH_USER_MODEL, verbose_name='使用者')),
            ],
            bases=('accounts.info',),
        ),
        migrations.CreateModel(
            name='ProfessorInfo',
            fields=[
                ('info_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.info')),
                ('telephone', models.CharField(max_length=20, verbose_name='辦公室電話')),
                ('title', models.CharField(max_length=20, verbose_name='職級')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='professor_info', to=settings.AUTH_USER_MODEL, verbose_name='使用者')),
            ],
            bases=('accounts.info',),
        ),
        migrations.CreateModel(
            name='ExpertInfo',
            fields=[
                ('info_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.info')),
                ('telephone', models.CharField(max_length=20, verbose_name='辦公室電話')),
                ('title', models.CharField(max_length=20, verbose_name='職稱')),
                ('address', models.CharField(max_length=100, verbose_name='聯絡地址')),
                ('bank_account', models.CharField(max_length=14, verbose_name='銀行(郵局)帳號')),
                ('company', models.CharField(max_length=50, verbose_name='任職公司')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='expert_info', to=settings.AUTH_USER_MODEL, verbose_name='使用者')),
            ],
            bases=('accounts.info',),
        ),
        migrations.CreateModel(
            name='AssistantInfo',
            fields=[
                ('info_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.info')),
                ('telephone', models.CharField(max_length=20, verbose_name='辦公室電話')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assistant_info', to=settings.AUTH_USER_MODEL, verbose_name='使用者')),
            ],
            bases=('accounts.info',),
        ),
    ]
