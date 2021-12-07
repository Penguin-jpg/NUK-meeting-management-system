from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from accounts.models import Participant
import datetime
import pytz

# 會議模型
class Meeting(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 名稱
    type = models.CharField(max_length=20)  # 種類
    date = models.DateTimeField()  # 日期
    location = models.CharField(max_length=100)  # 地點
    chairman = models.CharField(max_length=20)  # 主席(可能會改成relation field)
    minutes_taker = models.CharField(max_length=20)  # 記錄人員(可能會改成relation field)
    participants = models.ManyToManyField(
        Participant, related_name="meetings"
    )  # 與會人員(測試階段)

    def get_absolute_url(self):
        return reverse("meetings:meeting-detail", kwargs={"id": self.id})

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
