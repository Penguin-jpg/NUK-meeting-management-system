from typing import List
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from .models import Participant
from .forms import SignUpForm


# 使用者註冊
class UserRegisterView(CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")


# 使用者列表
class UserListView(ListView):
    model = User
    template_name = "user/user_list.html"
