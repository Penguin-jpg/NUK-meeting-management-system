from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from accounts.models import Participant
from datetime import datetime, timezone, tzinfo
import pytz

# 會議模型
class Meeting(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 名稱
    type = models.CharField(max_length=20)  # 種類
    date = models.DateTimeField()  # 日期
    location = models.CharField(max_length=100)  # 地點
    chairman = models.CharField(max_length=20)  # 主席(可能會改成relation field)
    minutes_taker = models.CharField(max_length=20)  # 記錄人員(可能會改成relation field)
    participants = models.ManyToManyField(Participant)  # 與會人員(測試階段)

    def get_absolute_url(self):
        return reverse("meetings:meeting-detail", kwargs={"id": self.id})

    # 取得url給日曆用
    @property
    def get_url(self):
        if self.name == "test4":
            print(self.date)
        url = reverse(
            "meeting-day",
            kwargs={
                "year": self.date.year,
                "month": self.date.month,
                "day": self.date.day,
            },
        )
        return f'<a href="{url}">當日會議</a>'


# 待解決，也許試試middleware
# https://www.itread01.com/article/1528957260.html
@receiver(post_save, sender=Meeting)
def change_to_local_timezone(sender, instance, created, **kwargs):
    if created:
        date = instance.date
        date = date.replace(tzinfo=None)
        print(date)
        instance.date = pytz.timezone(settings.TIME_ZONE).localize(date)
        print(instance.date)
        instance.save()
