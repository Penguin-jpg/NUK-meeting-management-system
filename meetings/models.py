import base64
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    To,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
    ContentId,
)
import os
import random
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
    participants = models.ManyToManyField(Participant, related_name="meetings", verbose_name="與會人員")
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
        return reverse("meeting-detail", kwargs={"id": self.id})

    def meeting_begins(self):
        # 需要用timezone aware的時間進行比較
        return timezone.now() > self.date

    def encode_attachment(self, file_path):
        # 把附件encode才能用sendgrid傳
        with open(file_path, "rb") as file:
            data = file.read()
            file.close()
        encoded = base64.b64encode(data).decode()

        attachment = Attachment(
            file_content=FileContent(encoded),
            file_type=FileType("application/pdf"),
            file_name=FileName(os.path.basename(file_path)),
            disposition=Disposition("attachment"),
            content_id=ContentId(str(random.randint(1, 10000))),
        )
        return attachment

    # 寄出開會通知
    def send_meeting_notification(self):
        participants = self.participants.all()
        formatted_date = self.date.strftime("%Y/%m/%d %H:%M")
        to_emails = [
            To(
                email=participant.email,
                dynamic_template_data={
                    "name": participant.get_full_name(),
                    "meeting_name": self.name,
                    "meeting_date": formatted_date,
                    "meeting_location": self.location,
                },
            )
            for participant in participants
        ]
        message = Mail(
            from_email=settings.EMAIL_HOST_USER,
            to_emails=to_emails,
            subject="高雄大學資訊工程學系會議管理系統 - 會議通知",
        )
        message.template_id = "d-a68207684c2c4fdca7f58fe1f4edc3d2"

        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    # 寄出開會結果
    def send_meeting_resolution(self):
        participants = self.participants.all()
        discussions_data = []
        announcements_data = []

        for discussion in self.discussions.all():
            discussions_data.append(
                {
                    "topic": discussion.topic,
                    "description": discussion.description,
                    "resolution": discussion.resolution,
                }
            )
        for announcement in self.announcements.all():
            announcements_data.append({"content": announcement.content})

        attachments = [self.encode_attachment(os.path.join("media", appendix.file.name)) for appendix in self.appendices.all()]
        formatted_date = self.date.strftime("%Y/%m/%d %H:%M")
        to_emails = [
            To(
                email=participant.email,
                dynamic_template_data={
                    "name": participant.get_full_name(),
                    "meeting_name": self.name,
                    "meeting_type": self.get_type_display(),
                    "meeting_date": formatted_date,
                    "meeting_location": self.location,
                    "chairman": self.chairman.get_full_name(),
                    "minutes_taker": self.minutes_taker.get_full_name(),
                    "announcements": announcements_data,
                    "discussions": discussions_data,
                },
            )
            for participant in participants
        ]
        message = Mail(
            from_email=settings.EMAIL_HOST_USER,
            to_emails=to_emails,
            subject="高雄大學資訊工程學系會議管理系統 - 開會結果通知",
        )
        message.template_id = "d-0d294c8542b94b72b8e4c73877fb2b7d"
        message.attachment = attachments

        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

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
