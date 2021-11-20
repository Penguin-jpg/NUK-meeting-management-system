from django.db import models
from django.urls import reverse
import uuid

# 會議模型
class Meeting(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )  # uuid(當作每個會議的獨特編號)
    name = models.CharField(max_length=100, unique=True)  # 名稱
    type = models.CharField(max_length=20, null=False)  # 種類
    date = models.DateField(null=False)  # 日期
    location = models.CharField(max_length=100, null=False)  # 地點
    chairman = models.CharField(max_length=20, null=False)  # 主席
    minutes_taker = models.CharField(max_length=20, null=False)  # 記錄人員

    def get_absolute_url(self):
        return reverse("meetings:meeting-detail", kwargs={"id": self.id})
