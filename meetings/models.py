from django.db import models
from django.urls import reverse
from accounts.models import Participant
import datetime

# 會議模型
class Meeting(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="會議名稱")
    type = models.CharField(max_length=20, verbose_name="會議種類")
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
        print(self.date)
        return datetime.datetime.now() > self.date

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
    meeting = models.ForeignKey(Meeting, on_delete=models.DO_NOTHING, verbose_name="會議")
    participant = models.ForeignKey(
        Participant, on_delete=models.DO_NOTHING, verbose_name="與會人員"
    )
    attend = models.BooleanField(default=False, verbose_name="出席")
