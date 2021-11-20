from django.db import models
from django.contrib.auth.models import User

THEME = (("淺色模式", "light"), ("黑暗模式", "dark"))


class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mode = models.CharField(max_length=10, choices=THEME, default="黑暗模式")

    def __str__(self):
        return self.mode
