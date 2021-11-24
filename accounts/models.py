from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField


SEX = ((-1, ""), (0, "女性"), (1, "男性"))
TYPE = ((-1, "無"), (0, "業界專家"), (1, "學生代表"), (2, "校外老師"), (3, "系助理"), (4, "系上老師"))


class Participant(AbstractUser):
    sex = models.IntegerField(choices=SEX, default=-1)  # 性別
    type = models.IntegerField(choices=TYPE, default=-1)  # 與會人員的種類

    class Meta:
        permissions = [
            ("look_up_meeting_minutes", "查詢會議紀錄"),
            ("view_meeting_minutes", "觀看會議紀錄"),
            ("request_for_modifying_meeting_minutes", "發出會議紀錄修改請求"),
            ("create_meeting", "產生新的會議資料"),
            ("edit_meeting", "編輯會議資料"),
            ("create_extempore_motion", "新增臨時動議"),
            ("mail_result", "寄出開會結果"),
        ]

    def __str__(self):
        return self.last_name + self.first_name


# 使用者的簡介，所以用一對一的關係連結
class Profile(models.Model):
    email = models.EmailField()  # email
    phone = PhoneNumberField(region="TW")  # 連絡電話
    user = models.OneToOneField(Participant, on_delete=models.CASCADE)  # 對應的使用者

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
class ExpertProfile(Profile):
    company = models.CharField(max_length=50)  # 任職公司
    title = models.CharField(max_length=20)  # 職稱
    telephone = PhoneNumberField(region="TW")  # 辦公室電話
    address = models.CharField(max_length=100)  # 聯絡地址
    bank_account = models.CharField(max_length=14)  # 銀行帳號

    def get_absolute_url(self):
        return reverse("accounts:expert-profile", kwargs={"id": self.id})


# 學生代表
class StudentRepresentativeProfile(Profile):
    student_id = models.CharField(max_length=15, primary_key=True)  # 學號
    school_system = models.CharField(max_length=10)  # 學制
    grade = models.CharField(max_length=10)  # 年級

    def get_absolute_url(self):
        return reverse(
            "accounts:student-representative-profile", kwargs={"id": self.id}
        )


# 校外老師
class ExternalTeacherProfile(Profile):
    school = models.CharField(max_length=50)  # 任職學校
    department = models.CharField(max_length=20)  # 系所
    title = models.CharField(max_length=20)
    telephone = PhoneNumberField(region="TW")
    address = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=14)

    def get_absolute_url(self):
        return reverse("accounts:external-teacher-profile", kwargs={"id": self.id})


# 系助理
class AssistantProfile(Profile):
    telephone = PhoneNumberField(region="TW")

    def get_absolute_url(self):
        return reverse("accounts:assistant-profile", kwargs={"id": self.id})


# 系上老師
class ProfessorProfile(Profile):
    title = models.CharField(max_length=20)
    telephone = PhoneNumberField(region="TW")

    def get_absolute_url(self):
        return reverse("profiles:professor-profile", kwargs={"id": self.id})
