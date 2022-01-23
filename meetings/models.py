from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_save
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from accounts.models import Participant
import datetime
import os

TYPE = ((0, "系務會議"), (1, "系教評會"), (2, "系課程委員會"), (3, "招生暨學生事務委員會"), (4, "系發展委員會"))

# 用來找出數字對應的字串
TYPE_MAP = {
    0: "系務會議",
    1: "系教評會",
    2: "系課程委員會",
    3: "招生暨學生事務委員會",
    4: "系發展委員會",
}

# 會議模型
class Meeting(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="會議名稱")
    type = models.IntegerField(choices=TYPE, default=0, verbose_name="會議種類")
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
    attendance_record = models.ManyToManyField(
        Participant,
        through="Attendance",
        through_fields=("meeting", "participant"),
        verbose_name="出席紀錄",
        related_name="attendance",
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
        return reverse("meetings:meeting-detail", kwargs={"id": self.id})

    def get_meeting_type(self):
        return TYPE_MAP[self.type]

    def meeting_begins(self):
        # 需要用timezone aware的時間進行比較
        return timezone.now() > self.date

    def send_meeting_notification(self):
        formatted_date = self.date.strftime("%Y/%m/%d %H:%M")  # 格式化日期
        # 可能會改用djang-template-mail
        send_mail(
            "高雄大學會議管理系統 - 會議通知",  # 標題
            f"您好，您參加的會議「{self.name}」（{self.get_meeting_type()}）將在 {formatted_date} 於{self.location}舉行",  # 內容
            settings.EMAIL_HOST_USER,  # 寄信人
            [participant.email for participant in self.participants.all()],  # 　收信人
            fail_silently=True,
        )
        # print("sent!")
        # message = get_template("meetings/email_template.html").render(
        #     context={"meeting": self, "formatted_date": formatted_date}
        # )
        # mail = EmailMessage(
        #     subject="高雄大學會議管理系統 - 會議通知",  # 標題
        #     body=message,  # 內容
        #     from_email=settings.EMAIL_HOST_USER,  # 　寄件人
        #     to=[participant.email for participant in self.participants.all()],  # 收信人
        # )
        # mail.content_subtype("html")  # 使用html
        # return mail.send()

    # 寄出開會結果
    def send_meeting_resolution(self):
        formatted_date = self.date.strftime("%Y/%m/%d %H:%M")  # 格式化日期
        content = ""

        for i, discussion in enumerate(self.discussions.all()):
            content += (
                f"案由{i + 1}：{discussion.topic}\n" + f"決議：{discussion.resolution}\n\n"
            )

        send_mail(
            "高雄大學會議管理系統 - 會議結果通知",  # 標題
            f"您好，您參加的會議「{self.name}」（{self.get_meeting_type()}）的會議結果如下：\n\n"
            + content,  # 內容
            settings.EMAIL_HOST_USER,  # 寄信人
            [participant.email for participant in self.participants.all()],  # 　收信人
            fail_silently=True,
        )

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
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="會議",
        related_name="attendance",
    )
    participant = models.ForeignKey(
        Participant,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="與會人員",
        related_name="attendance_records",
    )
    attend = models.BooleanField(default=False, verbose_name="出席")


# 修改請求
class EditRequest(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="會議",
        related_name="edit_requests",
    )
    participant = models.ForeignKey(
        Participant,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="與會人員",
        related_name="requests",
    )
    content = models.TextField(blank=False, verbose_name="內容")


# 臨時動議
class ExtemporeMotion(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="會議",
        related_name="extempore_motions",
    )
    proposer = models.CharField(max_length=100, verbose_name="提案人")
    content = models.CharField(max_length=500, verbose_name="內容")


# 報告事項
class Announcement(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="會議",
        related_name="announcements",
    )
    content = models.CharField(max_length=500, verbose_name="內容")


# 討論事項
class Discussion(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="會議",
        related_name="discussions",
    )
    topic = models.CharField(max_length=25, verbose_name="案由")
    description = models.CharField(max_length=500, verbose_name="說明")
    resolution = models.CharField(max_length=150, default="無", verbose_name="決議")


# 附件
class Appendix(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="會議",
        related_name="appendices",
    )
    provider = models.CharField(max_length=100, verbose_name="提供者")
    file = models.FileField(upload_to="files", verbose_name="檔案")

    # 取得檔案名稱(只有檔名，不包含路徑)
    def get_file_name(self):
        return os.path.basename(self.file.name)


# 建立或更新會議後寄出會議通知
# @receiver(post_save, sender=Meeting)
# def post_save_send_meeting_notification(sender, instance, created, **kwargs):
#     instance.send_meeting_notification()


# 刪除資料夾內附件
@receiver(post_delete, sender=Appendix)
def post_delete_delete_local_file(sender, instance, *args, **kwargs):
    try:
        instance.file.delete(save=False)
    except:
        print("There's an error occured while trying to delete file.")


# 更新資料夾內附件
@receiver(pre_save, sender=Appendix)
def pre_save_update_local_file(sender, instance, *args, **kwargs):
    try:
        old_file = instance.__class__.objects.get(id=instance.id).file.path
        try:
            new_file = instance.file.path
        except:
            new_file = None
        if new_file != old_file:
            if os.path.exists(old_file):
                os.remove(old_file)
    except:
        print("There's an error occured while trying to update file.")
