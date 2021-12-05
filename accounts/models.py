from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, Group
from django.contrib.auth.hashers import make_password
from django.apps import apps
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


SEX = ((0, "女性"), (1, "男性"), (2, "其他"))
TYPE = ((0, "業界專家"), (1, "學生代表"), (2, "校外老師"), (3, "系助理"), (4, "系上老師"))


class ParticipantManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)


class Participant(AbstractUser):
    objects = ParticipantManager()  # User Manager
    email = models.EmailField(blank=False, unique=True)  # 電子信箱
    type = models.IntegerField(choices=TYPE, default=0)  # 與會人員的種類

    USERNAME_FIELD = "email"  # 使用email登入
    REQUIRED_FIELDS = ["username"]

    class Meta:
        permissions = [
            ("request_for_modifying_meeting_minutes", "發出會議紀錄修改請求"),
            ("create_extempore_motion", "新增臨時動議"),
            ("mail_result", "寄出開會結果"),
        ]

    def __str__(self):
        return self.last_name + self.first_name

    def get_absolute_url(self):
        return reverse("accounts:user-detail", kwargs={"id": self.id})

    def get_full_name(self):
        return self.last_name + self.first_name

    # 檢查類別
    def is_expert(self):
        return self.type == 0

    def is_student(self):
        return self.type == 1

    def is_teacher(self):
        return self.type == 2

    def is_assistant(self):
        return self.type == 3

    def is_professor(self):
        return self.type == 4

    def get_identity(self):
        if self.type == 0:
            return "業界專家"
        elif self.type == 1:
            return "學生代表"
        elif self.type == 2:
            return "校外老師"
        elif self.type == 3:
            return "系助理"
        else:
            return "系上老師"


# 使用者的簡介，所以用一對一的關係連結
# 會使用一個包含所有欄位的Profile，再透過type來分類
class Profile(models.Model):
    # 共通的屬性
    user = models.OneToOneField(
        Participant, null=True, on_delete=models.CASCADE
    )  # 對應的使用者
    sex = models.IntegerField(choices=SEX, default=2)  # 性別
    # phone = PhoneNumberField(region="TW")  # 連絡電話(暫時先不用PhoneNumberField)
    phone = models.CharField(max_length=20)  # 連絡電話

    # 業界專家、校外老師、系助理、系上老師共通的屬性
    # telephone = PhoneNumberField(region="TW")  # 辦公室電話(暫時先不用PhoneNumberField)
    telephone = models.CharField(max_length=20)  # 辦公室電話

    # 業界專家、校外老師、系上老師共通的屬性
    title = models.CharField(max_length=20)  # 職稱

    # 業界專家、校外老師共通的屬性
    address = models.CharField(max_length=100)  # 聯絡地址
    bank_account = models.CharField(max_length=14)  # 銀行帳號

    # 業界專家的屬性
    company = models.CharField(max_length=50)  # 任職公司

    # 校外老師的屬性
    school = models.CharField(max_length=50)  # 任職學校
    department = models.CharField(max_length=20)  # 系所

    # 學生代表的屬性
    student_id = models.CharField(max_length=15)  # 學號
    school_system = models.CharField(max_length=10)  # 學制
    grade = models.CharField(max_length=10)  # 年級

    def get_absolute_url(self):
        return reverse("accounts:user-profile", kwargs={"id": self.id})

    def get_sex(self):
        if self.sex == 0:
            return "女性"
        elif self.sex == 1:
            return "男性"
        else:
            return "其他"

    def get_all_field(self):
        if self.user.is_expert():
            field_map = {
                "性別": self.get_sex,
                "連絡電話": self.phone,
                "任職公司": self.company,
                "職稱": self.title,
                "辦公室電話": self.telephone,
                "聯絡地址": self.address,
                "銀行(郵局)帳號": self.bank_account,
            }
        elif self.user.is_student():
            field_map = {
                "性別": self.get_sex,
                "連絡電話": self.phone,
                "學號": self.student_id,
                "學制": self.school_system,
                "年級": self.grade,
            }
        elif self.user.is_teacher():
            field_map = {
                "性別": self.get_sex,
                "連絡電話": self.phone,
                "任職學校": self.school,
                "系所": self.department,
                "職稱": self.title,
                "辦公室電話": self.telephone,
                "聯絡地址": self.address,
                "銀行(郵局)帳號": self.bank_account,
            }
        elif self.user.is_assistant():
            field_map = {
                "性別": self.get_sex,
                "連絡電話": self.phone,
                "辦公室電話": self.telephone,
            }
        else:
            field_map = {
                "性別": self.get_sex,
                "連絡電話": self.phone,
                "職級": self.title,
                "辦公室電話": self.telephone,
            }

        return field_map


# 建立使用者後加入群組(待研究，目前沒成功)
@receiver(post_save, sender=Participant)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        # if instance.type == 3:
        # group = Group.objects.get(name="operators")
        # else:
        group = Group.objects.get(name="normal_participants")
        instance.groups.add(group)
        instance.save()


# 建立使用者後新增簡介
@receiver(post_save, sender=Participant)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance).save()
