from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import os
from accounts.models import Participant
from utils.choices import MEETING_TYPES
from utils.email_thread import EmailThread

# 會議
class Meeting(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="會議名稱")
    type = models.IntegerField(choices=MEETING_TYPES, default=0, verbose_name="會議種類")
    date = models.DateTimeField(verbose_name="開會日期")
    location = models.CharField(max_length=100, verbose_name="會議地點")
    chairman = models.ForeignKey(
        Participant,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="主席",
        related_name="host_meeting",
    )
    minutes_taker = models.ForeignKey(
        Participant,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="記錄人員",
        related_name="take_minutes_meeting",
    )
    participants = models.ManyToManyField(
        Participant, related_name="meetings", verbose_name="與會人員"
    )
    speech = models.TextField(max_length=500, default="略", verbose_name="主席致詞")
    is_archived = models.BooleanField(default=False, verbose_name="歸檔")
    attendance = models.ManyToManyField(
        Participant,
        through="Attendance",
        through_fields=("meeting", "participant"),
        verbose_name="出席紀錄",
        related_name="attendances",
    )
    edit_request = models.ManyToManyField(
        Participant,
        through="EditRequest",
        through_fields=("meeting", "participant"),
        verbose_name="修改請求",
        related_name="edit_requests",
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("meeting-detail", kwargs={"pk": self.id})

    def meeting_begins(self):
        # 需要用timezone aware的時間進行比較
        return timezone.now() > self.date

    # 寄出開會通知
    def send_meeting_notification(self):
        context = {"participants": self.participants}  # 暫定的而已，可以改
        EmailThread(
            self,
            "高雄大學資訊工程學系會議管理系統 - 會議通知",
            "emails/notification_template.html",
            context,
        ).start()

    # 寄出開會結果
    def send_meeting_resolution(self):
        context = {"participants": self.participants}
        EmailThread(
            self,
            "高雄大學資訊工程學系會議管理系統 - 會議結果通知",
            "emails/resolution_template.html",
            context,
        )

        # content = ""
        # for i, discussion in enumerate(self.discussions.all()):
        #     content += (
        #         f"案由{i + 1}：{discussion.topic}\n" + f"決議：{discussion.resolution}\n\n"
        #     )

    # 取得url給日曆用
    @property
    def get_url(self):
        date = self.date
        # 如果要啟動時區，則需加上下面兩行
        # offset = datetime.timedelta(hours=8)  # UTC和台北時間差8小時
        # date = date + offset  # 加上時差轉成台北時間

        url = reverse(
            "meeting-day",
            kwargs={
                "year": date.year,
                "month": date.month,
                "day": date.day,
            },
        )
        return f'<a href="{url}">當日會議</a>'


# 出席紀錄
class Attendance(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        verbose_name="會議",
        related_name="meeting_attendance",
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        verbose_name="與會人員",
        related_name="attendance_records",
    )
    attend = models.BooleanField(default=False, verbose_name="出席")


# 修改請求
class EditRequest(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        verbose_name="會議",
        related_name="edit_requests",
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        verbose_name="與會人員",
        related_name="requests",
    )
    content = models.TextField(blank=False, verbose_name="內容")


# 報告事項
class Announcement(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        verbose_name="會議",
        related_name="announcements",
    )
    content = models.TextField(max_length=500, verbose_name="內容")


# 討論事項
class Discussion(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        verbose_name="會議",
        related_name="discussions",
    )
    topic = models.CharField(max_length=25, verbose_name="案由")
    description = models.TextField(max_length=500, verbose_name="說明")
    resolution = models.TextField(max_length=150, default="無", verbose_name="決議")


# 附件
class Appendix(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        verbose_name="會議",
        related_name="appendices",
    )
    provider = models.CharField(max_length=100, verbose_name="提供者")
    file = models.FileField(upload_to="files", verbose_name="檔案")

    # 取得檔案名稱(只有檔名，不包含路徑)
    def get_file_name(self):
        return os.path.basename(self.file.name)


# 會議建議
class Advice(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        verbose_name="會議",
        related_name="advices",
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        verbose_name="與會人員",
        related_name="meeting_advices",
    )
    advice = models.TextField(blank=False, verbose_name="建議")


@receiver(post_save, sender=Meeting)
def post_save_send_notification(sender, instance, *args, **kwargs):
    instance.send_meeting_notification()


# 刪除資料夾內附件
@receiver(post_delete, sender=Appendix)
def post_delete_delete_local_file(sender, instance, *args, **kwargs):
    if instance.file:
        instance.file.delete(save=False)


# 更新資料夾內附件
@receiver(pre_save, sender=Appendix)
def pre_save_update_local_file(sender, instance, *args, **kwargs):
    try:
        old_file = Appendix.objects.get(id=instance.id).file.path

        try:
            new_file = instance.file.path
        except:
            new_file = None

        if new_file != old_file:
            if os.path.exists(old_file):
                os.remove(old_file)
    except:
        print("There's an error occured while trying to update file.")
