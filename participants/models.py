from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField

# 把與會人員當作使用者的簡介的概念，所以用一對一的關係連結

SEX = ((0, "女性"), (1, "男性"))


class Participant(models.Model):
    sex = models.IntegerField(choices=SEX)  # 性別
    identity = models.CharField(max_length=50)  # 身分
    email = models.EmailField()  # email
    phone = PhoneNumberField(region="TW")  # 連絡電話
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)  # 對應的使用者

    # 建立使用者的同時新增簡介(待研究)
    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Participant.objects.create(user=instance)

    # 儲存使用者的簡介
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()


# 業界專家
class Expert(Participant):
    company = models.CharField(max_length=50)  # 任職公司
    title = models.CharField(max_length=20)  # 職稱
    telephone = PhoneNumberField(region="TW")  # 辦公室電話
    address = models.CharField(max_length=100)  # 聯絡地址
    bank_account = models.CharField(max_length=14)  # 銀行帳號


# 學生代表
class StudentRepresentative(Participant):
    student_id = models.CharField(max_length=15, primary_key=True)  # 學號
    school_system = models.CharField(max_length=10)  # 學制
    grade = models.CharField(max_length=10)  # 年級


# 校外老師
class Teacher(Participant):
    school = models.CharField(max_length=50)  # 任職學校
    department = models.CharField(max_length=20)  # 系所
    title = models.CharField(max_length=20)  # 職稱
    telephone = PhoneNumberField(region="TW")  # 辦公室電話
    address = models.CharField(max_length=100)  # 聯絡地址
    bank_account = models.CharField(max_length=14)  # 銀行帳號


# 系助理
class Assistant(Participant):
    telephone = PhoneNumberField(region="TW")  # 辦公室電話


# 系上老師
class Professor(Participant):
    title = models.CharField(max_length=20)  # 職稱
    telephone = PhoneNumberField(region="TW")  # 辦公室電話
