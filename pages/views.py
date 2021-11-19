from django.shortcuts import render
from user_settings.models import UserSetting


def home_view(request, *args, **kwargs):
    return render(request, "index.html", {})


def user_setting(request):
    if request.user.is_authenticated:
        setting = UserSetting.objects.filter(user=request.user)
    else:
        setting = None

    return render(request, "index.html", {"setting": setting})
