from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
from .models import Participant, Profile
from .forms import (
    SignUpForm,
    # ExpertEditForm,
    # StudentEditForm,
    # TeacherEditForm,
    # AssistantEditForm,
    # ProfessorEditForm,
    ProfileEditForm,
)

# 使用者註冊
class UserRegisterView(CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


# 使用者列表(可以更精緻，但暫時算完成)
class UserListView(ListView):
    model = Participant
    template_name = "accounts/user_list.html"


# 刪除使用者(可以更精緻，但暫時算完成)
class UserDeleteView(DeleteView):
    model = Participant
    template_name = "accounts/user_delete.html"
    success_url = reverse_lazy("login")

    def get_object(self):
        id = self.kwargs["id"]
        return get_object_or_404(Participant, id=id)


# 使用者個人資料
@login_required(login_url="login")
def user_profile_view(request):
    try:
        profile = Profile.objects.get(id=request.user.profile.id)
    except Profile.DoesNotExist:
        return render(request, "accounts/no_identity.html", {})

    # type = ((0, "業界專家"), (1, "學生代表"), (2, "校外老師"), (3, "系助理"), (4, "系上老師"))
    if profile.is_expert():
        identity = "業界專家"
    elif profile.is_student():
        identity = "學生代表"
    elif profile.is_teacher():
        identity = "校外老師"
    elif profile.is_assistant():
        identity = "系助理"
    elif profile.is_professor():
        identity = "系上老師"

    context = {"identity": identity, "profile": profile}

    return render(request, "accounts/user_profile.html", context)


# 編輯個人資料
@login_required(login_url="login")
def edit_profile_view(request):
    try:
        profile = Profile.objects.get(id=request.user.profile.id)
    except Profile.DoesNotExist:
        return render(request, "accounts/no_identity.html", {})

    form = ProfileEditForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect("user-profile")
    else:
        form = ProfileEditForm(instance=profile)

    context = {"form": form, "profile": profile}

    return render(request, "accounts/edit_profile.html", context)
