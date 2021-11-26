from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField


SEX = ((0, "女性"), (1, "男性"))
TYPE = ((0, "業界專家"), (1, "學生代表"), (2, "校外老師"), (3, "系助理"), (4, "系上老師"))


class Participant(AbstractUser):
    type = models.IntegerField(choices=TYPE, default=0)  # 與會人員的種類

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

    def get_absolute_url(self):
        return reverse("accounts:user-detail", kwargs={"id": self.id})


# TODO: 照著這篇的建議做 https://stackoverflow.com/questions/11335422/django-multiple-profiles
# 使用者的簡介，所以用一對一的關係連結
# 會使用一個包含所有欄位的Profile，再透過type來分類
class Profile(models.Model):
    # 共通的屬性
    user = models.OneToOneField(
        Participant, null=True, on_delete=models.CASCADE
    )  # 對應的使用者
    sex = models.IntegerField(choices=SEX, default=0)  # 性別
    email = models.EmailField()  # 電子信箱
    phone = PhoneNumberField(region="TW")  # 連絡電話

    # 業界專家、校外老師、系助理、系上老師共通的屬性
    telephone = PhoneNumberField(region="TW")  # 辦公室電話

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

    # 建立使用者的同時新增簡介
    @receiver(post_save, sender=Participant)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    # # 儲存使用者的簡介
    @receiver(post_save, sender=Participant)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    # 檢查類別
    def is_expert(self):
        return self.user.type == 0

    def is_student(self):
        return self.user.type == 1

    def is_teacher(self):
        return self.user.type == 2

    def is_assistant(self):
        return self.user.type == 3

    def is_professor(self):
        return self.user.type == 4

    def get_absolute_url(self):
        return reverse("accounts:user-profile", kwargs={"id": self.id})
