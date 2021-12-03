from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import Participant, Profile
from .forms import (
    SignUpForm,
    ProfileEditForm,
)

# 使用者註冊
def user_register_view(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "註冊成功!")
        return redirect("login")
    else:
        form = SignUpForm()

    context = {"form": form}

    return render(request, "registration/register.html", context)


# 使用者列表(可以更精緻，但暫時算完成)
@method_decorator(login_required(login_url="login"), name="dispatch")
class UserListView(ListView):
    model = Participant
    template_name = "accounts/user_list.html"


# 刪除使用者(可以更精緻，但暫時算完成)
@method_decorator(login_required(login_url="login"), name="dispatch")
@method_decorator(
    permission_required("accounts.delete_participant", raise_exception=True),
    name="dispatch",
)
class UserDeleteView(DeleteView):
    model = Participant
    template_name = "accounts/user_delete.html"
    success_url = reverse_lazy("login")

    def get_object(self):
        id = self.kwargs["id"]
        return get_object_or_404(Participant, id=id)


# 使用者個人資料
@login_required(login_url="login")
def user_profile_view(request, id):
    try:
        profile = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return render(request, "accounts/no_profile.html", {})

    form = ProfileEditForm(instance=profile)

    context = {"profile": profile, "form": form}

    return render(request, "accounts/user_profile.html", context)


# 編輯個人資料
@login_required(login_url="login")
@permission_required("accounts.change_profile", raise_exception=True)
def edit_profile_view(request, id):
    try:
        profile = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return render(request, "accounts/no_identity.html", {})

    form = ProfileEditForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
        messages.success(request, "修改成功!")
        return redirect("user-profile", id)
    else:
        # messages.error(request, "修改失敗")
        form = ProfileEditForm(instance=profile)

    context = {"form": form, "profile": profile}

    return render(request, "accounts/edit_profile.html", context)
