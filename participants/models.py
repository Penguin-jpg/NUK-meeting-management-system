from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

SEX = ((0, "Female"), (1, "Male"))

# Create your models here.
class Participant(models.Model):
    account = models.CharField(max_length=30, primary_key=True)  # 帳號
    password = models.CharField(max_length=50, null=False)  # 密碼
    name = models.CharField(max_length=20, null=False)  # 名稱
    sex = models.IntegerField(choices=SEX, null=False)  # 性別
    identity = models.CharField(max_length=50, null=False)  # 身分
    email = models.EmailField(null=False)  # email
    phone = PhoneNumberField(null=False, blank=False, region="TW")  # 連絡電話


# 業界專家
class Expert(Participant):
    company = models.CharField(max_length=50, null=False)  # 任職公司
    title = models.CharField(max_length=20, null=False)  # 職稱
    telephone = PhoneNumberField(null=False, blank=False, region="TW")  # 辦公室電話
    address = models.CharField(max_length=100, null=False)  # 聯絡地址
    bank_account = models.CharField(max_length=14, null=False)  # 銀行帳號


# 學生代表
class StudentRepresentative(Participant):
    student_id = models.CharField(max_length=15, primary_key=True, null=False)  # 學號
    school_system = models.CharField(max_length=10, null=False)  # 學制
    grade = models.CharField(max_length=10, null=False)  # 年級


# 校外老師
class Teacher(Participant):
    school = models.CharField(max_length=50, null=False)  # 任職學校
    department = models.CharField(max_length=20, null=False)  # 系所
    title = models.CharField(max_length=20, null=False)  # 職稱
    telephone = PhoneNumberField(null=False, blank=False, region="TW")  # 辦公室電話
    address = models.CharField(max_length=100, null=False)  # 聯絡地址
    bank_account = models.CharField(max_length=14, null=False)  # 銀行帳號


# 系助理
class Assistant(Participant):
    telephone = PhoneNumberField(null=False, blank=False, region="TW")  # 辦公室電話


# 系上老師
class Professor(Participant):
    title = models.CharField(max_length=20, null=False)  # 職稱
    telephone = PhoneNumberField(null=False, blank=False, region="TW")  # 辦公室電話
