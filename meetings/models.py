from django.db import models

# 會議模型
class Meeting(models.Model):
    name = models.CharField(max_length=100, primary_key=True, unique=True)  # 名稱
    type = models.CharField(max_length=20, null=False)  # 種類
    date = models.DateField(null=False)  # 日期
    location = models.CharField(max_length=100, null=False)  # 地點
    chairman = models.CharField(max_length=20, null=False)  # 主席
    minutes_taker = models.CharField(max_length=20, null=False)  # 記錄人員
