from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Participant
from .forms import SignUpForm

# 未完成(可能會改為generic)
def user_create_view(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        form.save()
        print(form.cleaned_data)
        return redirect("home")
    else:
        form = SignUpForm()  # 回歸成空的表格
        print("fail")
    context = {"form": form}
    return render(request, "registration/register.html", context)


def user_list_view(request):
    queryset = User.objects.all()
    context = {"users": queryset}
    return render(request, "user/user_list.html", context)
