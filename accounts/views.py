from typing import List
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from .models import (
    Participant,
    AssistantProfile,
    ExpertProfile,
    ProfessorProfile,
    StudentRepresentativeProfile,
    ExternalTeacherProfile,
)
from .forms import SignUpForm

# 使用者註冊
class UserRegisterView(CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


# 使用者列表
class UserListView(ListView):
    model = Participant
    template_name = "accounts/user_list.html"


# 使用者個人簡介 (未完成)
def user_profile_view(request, id):
    type = request.user.type
    user = Participant.objects.get(id=id)

    if type == -1 or user == None:
        return render(request, "accounts/no_identity.html", {})  # 這部分沒作用，不知道為啥
    else:
        # type = ((-1, "無"), (0, "業界專家"), (1, "學生代表"), (2, "校外老師"), (3, "系助理"), (4, "系上老師"))
        p_id = user.participant.id
        if type == 0:
            participant = get_object_or_404(ExpertProfile, id=p_id)
            identity = "expert"
        elif type == 1:
            participant = get_object_or_404(StudentRepresentativeProfile, id=p_id)
            identity = "student_representtative"
        elif type == 2:
            participant = get_object_or_404(ExternalTeacherProfile, id=p_id)
            identity = "external_teacher"
        elif type == 3:
            participant = get_object_or_404(AssistantProfile, id=p_id)
            identity = "assistant"
        elif type == 4:
            participant = get_object_or_404(ProfessorProfile, id=p_id)
            identity = "professor"

        context = {"participant": participant}

        return render(request, f"accounts/{identity}_profile.html", context)
