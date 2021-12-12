from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, Group
from django.contrib.auth.hashers import make_password
from django.apps import apps
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


SEX = ((0, "女性"), (1, "男性"), (2, "其他"))
IDENTITY = ((0, "業界專家"), (1, "學生代表"), (2, "校外老師"), (3, "系助理"), (4, "系上老師"))


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


# 與會人員(使用者)
class Participant(AbstractUser):
    objects = ParticipantManager()  # User Manager
    email = models.EmailField(blank=False, unique=True, verbose_name="電子信箱")
    identity = models.IntegerField(choices=IDENTITY, default=0, verbose_name="身分")
    sex = models.IntegerField(choices=SEX, default=2, verbose_name="性別")
    # phone = PhoneNumberField(region="TW")  # 連絡電話(暫時先不用PhoneNumberField)
    phone = models.CharField(max_length=20, verbose_name="連絡電話")

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

    # 取得全名
    def get_full_name(self):
        return self.last_name + self.first_name

    # 取得身分
    def get_identity(self):
        if self.identity == 0:
            return "業界專家"
        elif self.identity == 1:
            return "學生代表"
        elif self.identity == 2:
            return "校外老師"
        elif self.identity == 3:
            return "系助理"
        else:
            return "系上老師"

    # 取得性別
    def get_sex(self):
        if self.sex == 0:
            return "女性"
        elif self.sex == 1:
            return "男性"
        else:
            return "其他"

    # 取得個人資料
    def get_info(self):
        if self.identity == 0:
            return self.expert_info
        elif self.identity == 1:
            return self.student_info
        elif self.identity == 2:
            return self.teacher_info
        elif self.identity == 3:
            return self.assistant_info
        else:
            return self.professor_info


# 將不同的身分當作額外的model對應到使用者，當作他的個人資料
# 個人資料父類別
class Info(models.Model):
    # 取得所有欄位
    def get_all_fields(self):
        # 前三個欄位分別是id, info prt, user，不需要顯示
        fields = {
            field.verbose_name: field.value_from_object(self)
            for field in self._meta.get_fields()[3:]
        }
        # print(fields)
        return fields

    def get_absolute_url(self):
        return reverse("accounts:user-info", kwargs={"id": self.id})


# 業界專家
class ExpertInfo(Info):
    user = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name="expert_info",
        verbose_name="使用者",
    )
    # telephone = PhoneNumberField(region="TW")  # 辦公室電話(暫時先不用PhoneNumberField)
    telephone = models.CharField(max_length=20, verbose_name="辦公室電話")
    title = models.CharField(max_length=20, verbose_name="職稱")
    address = models.CharField(max_length=100, verbose_name="聯絡地址")
    bank_account = models.CharField(max_length=14, verbose_name="銀行(郵局)帳號")
    company = models.CharField(max_length=50, verbose_name="任職公司")


# 學生代表
class StudentInfo(Info):
    user = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name="student_info",
        verbose_name="使用者",
    )
    student_id = models.CharField(max_length=15, verbose_name="學號")
    school_system = models.CharField(max_length=10, verbose_name="學制")
    grade = models.CharField(max_length=10, verbose_name="年級")


# 校外老師
class TeacherInfo(Info):
    user = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name="teacher_info",
        verbose_name="使用者",
    )
    # telephone = PhoneNumberField(region="TW")  # 辦公室電話(暫時先不用PhoneNumberField)
    telephone = models.CharField(max_length=20, verbose_name="辦公室電話")
    title = models.CharField(max_length=20, verbose_name="職稱")
    address = models.CharField(max_length=100, verbose_name="聯絡地址")
    bank_account = models.CharField(max_length=14, verbose_name="銀行(郵局)帳號")
    school = models.CharField(max_length=50, verbose_name="任職學校")
    department = models.CharField(max_length=20, verbose_name="系所")


# 系助理
class AssistantInfo(Info):
    user = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name="assistant_info",
        verbose_name="使用者",
    )
    # telephone = PhoneNumberField(region="TW")  # 辦公室電話(暫時先不用PhoneNumberField)
    telephone = models.CharField(max_length=20, verbose_name="辦公室電話")


# 系上老師
class ProfessorInfo(Info):
    user = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name="professor_info",
        verbose_name="使用者",
    )
    # telephone = PhoneNumberField(region="TW")  # 辦公室電話(暫時先不用PhoneNumberField)
    telephone = models.CharField(max_length=20, verbose_name="辦公室電話")
    title = models.CharField(max_length=20, verbose_name="職級")


# 建立使用者後新增簡介
@receiver(post_save, sender=Participant)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        identity = instance.identity

        # 根據身分建立個人資料
        if identity == 0:
            info = ExpertInfo(user=instance)
        elif identity == 1:
            info = StudentInfo(user=instance)
        elif identity == 2:
            info = TeacherInfo(user=instance)
        elif identity == 3:
            info = AssistantInfo(user=instance)
        else:
            info = ProfessorInfo(user=instance)

        info.save()


# # 建立使用者後加入群組(待研究，目前沒成功)
# @receiver(post_save, sender=Participant)
# def add_user_to_group(sender, instance, created, **kwargs):
#     if created:
#         # if instance.type == 3:
#         # group = Group.objects.get(name="operators")
#         # else:
#         group = Group.objects.get(name="normal_participants")
#         instance.groups.add(group)
#         instance.save()
