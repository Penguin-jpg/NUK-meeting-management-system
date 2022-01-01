from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import *
from .forms import (
    SignUpForm,
    LoginForm,
    get_info_create_form,
)

# 選擇使用者身分
def user_choose_identity_view(request):
    return render(request, "registration/select_identity.html", {})


# 若沒有選擇身分就直接到註冊頁面時就顯示這個頁面
def no_identity_view(request):
    return render(request, "registration/no_identity.html", {})


# 若找不到使用者就顯示這個頁面
def user_not_found_view(request):
    return render(request, "accounts/user_not_found.html", {})


# 使用者註冊
def user_register_view(request):
    identity = request.GET.get("identity", None)

    if identity == None:
        return redirect("no-identity")

    identity = int(identity)
    form = SignUpForm(request.POST or None, initial={"identity": identity})

    if form.is_valid():
        form.save()
        user = Participant.objects.get(username=form.cleaned_data["username"])
        messages.success(request, "註冊成功!")
        # 註冊成功且登入後，將使用者導向到編輯個人資料
        return redirect("edit-info", user.id)
    else:
        form = SignUpForm(initial={"identity": identity})

    context = {"form": form}

    return render(request, "registration/register.html", context)


# 使用者登入
class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"


# 使用者登出
class UserLogoutView(LogoutView):
    template_name = "registration/logout.html"


# 使用者列表(可以更精緻，但暫時算完成)
@method_decorator(login_required(login_url="login"), name="dispatch")
class UserListView(ListView):
    model = Participant
    template_name = "accounts/user_list.html"


# 使用者個人資料
@login_required(login_url="login")
def user_info_view(request, id):
    try:
        user = Participant.objects.get(id=id)
    except Participant.DoesNotExist:
        return redirect("user-not-found")
    context = {"info": user.get_info()}
    return render(request, "accounts/user_info.html", context)


# 編輯使用者個人資料
@login_required(login_url="login")
@permission_required("accounts.change_info", raise_exception=True)
def edit_info_view(request, id):
    try:
        user = Participant.objects.get(id=id)
    except Participant.DoesNotExist:
        return redirect("user-not-found")
    form = get_info_create_form(request.POST or None, user)

    if form.is_valid():
        form.save()
        return redirect("user-info", user.id)
    else:
        form = get_info_create_form(request.POST or None, user)

    context = {"form": form}

    return render(request, "accounts/edit_info.html", context)


# 觀看參加過的會議紀錄
def meeting_record_view(request, id):
    try:
        user = Participant.objects.get(id=id)
    except Participant.DoesNotExist:
        return redirect("user-not-found")

    # 參加過的會議
    meetings = user.meetings.all()

    context = {"meetings": meetings}

    return render(request, "accounts/meeting_record.html", context)
