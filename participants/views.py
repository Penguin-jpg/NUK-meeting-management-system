from typing import List
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from .models import (
    Assistant,
    Participant,
    Expert,
    Professor,
    StudentRepresentative,
    Teacher,
)
from .forms import SignUpForm


# 使用者註冊
class UserRegisterView(CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


# 使用者列表
class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"


# 個人簡介(資料) (已可以根據identity進行動態轉換，但個別的網頁還沒完成)
def user_profile_view(request, id):
    type = request.user.participant.identity
    user = User.objects.get(id=id)

    if type == -1 or user == None:
        return render(request, "users/no_identity.html", {})  # 這部分沒作用，不知道為啥
    else:
        # type = ((-1, "無"), (0, "業界專家"), (1, "學生代表"), (2, "校外老師"), (3, "系助理"), (4, "系上老師"))
        p_id = user.participant.id
        if type == 0:
            participant = get_object_or_404(Expert, id=p_id)
            identity = "expert"
        elif type == 1:
            participant = get_object_or_404(StudentRepresentative, id=p_id)
            identity = "student_representtative"
        elif type == 2:
            participant = get_object_or_404(Teacher, id=p_id)
            identity = "teacher"
        elif type == 3:
            participant = get_object_or_404(Assistant, id=p_id)
            identity = "assistant"
        elif type == 4:
            participant = get_object_or_404(Professor, id=p_id)
            identity = "professor"

        context = {"participant": participant}

        return render(request, f"users/{identity}_detail.html", context)
