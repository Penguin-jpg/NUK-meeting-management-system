from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from utils.choices import SEX, IDENTITY


# 與會人員(使用者)
class Participant(AbstractUser):
    email = models.EmailField(blank=False, verbose_name="電子信箱")
    identity = models.IntegerField(choices=IDENTITY, default=0, verbose_name="身分")
    sex = models.IntegerField(choices=SEX, default=2, verbose_name="性別")
    phone = models.CharField(max_length=20, verbose_name="連絡電話")

    class Meta:
        permissions = [
            ("mail_result", "寄出開會結果"),
        ]

    def __str__(self):
        return self.last_name + self.first_name

    def get_absolute_url(self):
        return reverse("accounts:user-detail", kwargs={"id": self.id})

    # 取得全名
    def get_full_name(self):
        return self.last_name + self.first_name

    # 取得個人資料
    def get_profile(self):
        identity = self.identity
        if identity == 0:
            return self.expert_profile
        elif identity == 1:
            return self.student_profile
        elif identity == 2:
            return self.teacher_profile
        elif identity == 3:
            return self.assistant_profile
        else:
            return self.professor_profile


class Profile(models.Model):
    class Meta:
        abstract = True

    def get_fields(self):
        # 前兩個欄位不需要顯示id, profile ptr
        return {
            field.verbose_name: field.value_from_object(self)
            for field in self._meta.get_fields()[2:]
        }

    def get_absolute_url(self):
        return reverse("accounts:user-profile", kwargs={"pk": self.id})


# 業界專家
class ExpertProfile(Profile):
    user = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name="expert_profile",
        verbose_name="使用者",
    )
    telephone = models.CharField(max_length=20, verbose_name="辦公室電話")
    title = models.CharField(max_length=20, verbose_name="職稱")
    address = models.CharField(max_length=100, verbose_name="聯絡地址")
    bank_account = models.CharField(max_length=14, verbose_name="銀行(郵局)帳號")
    company = models.CharField(max_length=50, verbose_name="任職公司")


# 學生代表
class StudentProfile(Profile):
    user = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name="student_profile",
        verbose_name="使用者",
    )
    student_id = models.CharField(max_length=15, verbose_name="學號")
    school_system = models.CharField(max_length=10, verbose_name="學制")
    grade = models.CharField(max_length=10, verbose_name="年級")


# 校外老師
class TeacherProfile(Profile):
    user = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
        verbose_name="使用者",
    )
    telephone = models.CharField(max_length=20, verbose_name="辦公室電話")
    title = models.CharField(max_length=20, verbose_name="職稱")
    address = models.CharField(max_length=100, verbose_name="聯絡地址")
    bank_account = models.CharField(max_length=14, verbose_name="銀行(郵局)帳號")
    school = models.CharField(max_length=50, verbose_name="任職學校")
    department = models.CharField(max_length=20, verbose_name="系所")


# 系助理
class AssistantProfile(Profile):
    user = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name="assistant_profile",
        verbose_name="使用者",
    )
    telephone = models.CharField(max_length=20, verbose_name="辦公室電話")


# 系上老師
class ProfessorProfile(Profile):
    user = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name="professor_profile",
        verbose_name="使用者",
    )
    telephone = models.CharField(max_length=20, verbose_name="辦公室電話")
    title = models.CharField(max_length=20, verbose_name="職級")


# 根據使用者身分建立個人資料
@receiver(post_save, sender=Participant)
def post_save_create_user_profile(sender, instance, created, **kwargs):
    if created:
        identity = instance.identity

        # 根據身分建立個人資料
        if identity == 0:
            ExpertProfile(user=instance).save()
        elif identity == 1:
            StudentProfile(user=instance).save()
        elif identity == 2:
            TeacherProfile(user=instance).save()
        elif identity == 3:
            AssistantProfile(user=instance).save()
        else:
            ProfessorProfile(user=instance).save()
