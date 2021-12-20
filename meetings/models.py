from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from accounts.models import Participant
import datetime

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
    chairman = models.CharField(max_length=20, verbose_name="主席")  # 可能會改成relation field
    minutes_taker = models.CharField(
        max_length=20, verbose_name="記錄人員"
    )  # 可能會改成relation field
    participants = models.ManyToManyField(
        Participant, related_name="meetings", verbose_name="與會人員"
    )  # 測試階段
    speech = models.CharField(max_length=500, default="略", verbose_name="主席致詞")
    attendance_record = models.ManyToManyField(
        Participant,
        through="Attendance",
        through_fields=("meeting", "participant"),
        verbose_name="出席紀錄",
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("meetings:meeting-detail", kwargs={"id": self.id})

    def meeting_begins(self):
        # 需要用timezone aware的時間進行比較
        return timezone.now() > self.date

    def get_type(self):
        return TYPE_MAP[self.type]

    # 取得url給日曆用
    @property
    def get_url(self):
        date = self.date
        offset = datetime.timedelta(hours=8)  # UTC和台北時間差8小時
        date = date + offset  # 加上時差轉成台北時間

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
        Meeting, null=True, on_delete=models.SET_NULL, verbose_name="會議"
    )
    participant = models.ForeignKey(
        Participant, on_delete=models.DO_NOTHING, verbose_name="與會人員"
    )
    attend = models.BooleanField(default=False, verbose_name="出席")


# 臨時動議
class ExtemporeMotion(models.Model):
    meeting = models.ForeignKey(Meeting, null=True, on_delete=models.SET_NULL, verbose_name="會議")
    proposer = models.CharField(max_length=100, verbose_name="提案人")
    content = models.CharField(max_length=500, verbose_name="內容")


# 報告事項
class Announcement(models.Model):
    meeting = models.ForeignKey(Meeting, null=True, on_delete=models.SET_NULL, verbose_name="會議")
    content = models.CharField(max_length=500, verbose_name="內容")


# 討論事項
class Discussion(models.Model):
    meeting = models.ForeignKey(Meeting, null=True, on_delete=models.SET_NULL, verbose_name="會議")
    topic = models.CharField(max_length=25, verbose_name="案由")
    description = models.CharField(max_length=500, verbose_name="說明")
    resolution = models.CharField(max_length=150, verbose_name="決議")
