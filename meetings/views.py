from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from crispy_forms.layout import Layout, Field, Submit
from .models import *
from .forms import *
from utils.base_form_helper import BaseFormHelper
from utils.formsets import (
    AttendanceFormSet,
    AnnouncementFormSet,
    DiscussionFormSet,
    AppendixFormSet,
)

# 建立會議
@method_decorator(
    [
        login_required(login_url="login"),
        permission_required("meetings.add_meeting", raise_exception=True),
    ],
    name="dispatch",
)
class MeetingCreateView(CreateView):
    model = Meeting
    template_name = "meetings/meeting_create.html"
    form_class = MeetingCreateForm
    success_url = reverse_lazy("meeting-list")


# 會議列表
@method_decorator(login_required(login_url="login"), name="dispatch")
class MeetingListView(ListView):
    model = Meeting
    template_name = "meetings/meeting_list.html"

    def get_queryset(self):
        return Meeting.objects.filter(is_archived=False)


# 會議細節(議程)
@method_decorator(login_required(login_url="login"), name="dispatch")
class MeetingDetailView(DetailView):
    model = Meeting
    template_name = "meetings/meeting_detail.html"


# 編輯會議資料
@method_decorator(
    [
        login_required(login_url="login"),
        permission_required("meetings.change_meeting", raise_exception=True),
    ],
    name="dispatch",
)
class MeetingUpdateView(UpdateView):
    model = Meeting
    template_name = "meetings/edit_meeting.html"
    form_class = MeetingEditForm

    def form_valid(self, form):
        meeting = form.instance
        old_participants = meeting.participants.all()
        new_participants = form.cleaned_data["participants"]

        # 只在舊的人員名單內才有
        only_in_old = old_participants.difference(new_participants)
        # 只在新的人員名單內才有
        only_in_new = new_participants.difference(old_participants)
        old_size = only_in_old.count()
        new_size = only_in_new.count()
        index = 0
        # print("old: ", old_participants)
        # print("new: ", new_participants)

        if old_size > new_size:
            for old_participant in only_in_old:
                if index < new_size:
                    # 將不參加的舊人員出席紀錄改為新的人員
                    old_participant.attendance_records.update(
                        participant=only_in_new[index]
                    )
                    index += 1
                else:
                    # 多餘的刪掉
                    old_participant.attendance_records.get(meeting=meeting).delete()
        else:
            for old_participant in only_in_old:
                if index < old_size:
                    old_participant.attendance_records.update(
                        participant=only_in_new[index]
                    )
                    index += 1
                else:
                    break

            # 多出來的新人員要額外新增出席紀錄
            for i in range(index, new_size):
                Attendance.objects.create(meeting=meeting, participant=only_in_new[i])

        form.save()
        return super().form_valid(form)


# 刪除會議資料
@method_decorator(
    [
        login_required(login_url="login"),
        permission_required("meetings.delete_meeting", raise_exception=True),
    ],
    name="dispatch",
)
class MeetingDeleteView(DeleteView):
    model = Meeting
    template_name = "meetings/meeting_delete.html"
    success_url = reverse_lazy("meeting-list")


# 顯示某個會議的所有與會人員
@login_required(login_url="login")
def meeting_participants_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Meeting.DoesNotExist:
        return redirect("meeting-not-found")

    context = {
        "participants": meeting.participants.all(),
    }

    return render(request, "meetings/meeting_participants.html", context)


# 顯示歸檔的會議
@method_decorator(login_required(login_url="login"), name="dispatch")
class ArchivedMeetingListView(ListView):
    model = Meeting
    template_name = "meetings/archived_meeting.html"

    def get_queryset(self):
        return Meeting.objects.filter(is_archived=True)


# 編輯人員出席紀錄
# https://punchagan.muse-amuse.in/blog/django-modelformset-multiple-saves/
@login_required(login_url="login")
@permission_required("meetings.change_attendance", raise_exception=True)
def edit_attendance_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Meeting.DoesNotExist:
        return redirect("meeting-not-found")

    formset = AttendanceFormSet(request.POST or None, instance=meeting)
    helper = BaseFormHelper()
    helper.form_id = "edit-attendance-form"
    helper.layout = Layout(
        Field("participant"),
        Field("attend"),
    )
    helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))

    if formset.is_valid():
        formset.save()
        return redirect("meeting-detail", id)
    else:
        formset = AttendanceFormSet(instance=meeting)

    context = {"formset": formset, "helper": helper}

    return render(request, "meetings/edit_attendance.html", context)


# 顯示所有修改請求
@login_required(login_url="login")
@permission_required("meetings.view_editrequest", raise_exception=True)
def request_list_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Meeting.DoesNotExist:
        return redirect("meeting-not-found")

    edit_requests = meeting.edit_requests.all()

    context = {"edit_requests": edit_requests}

    return render(request, "meetings/request_list.html", context)


# 編輯修改請求
@login_required(login_url="login")
def edit_request_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Meeting.DoesNotExist:
        return redirect("meeting-not-found")

    user = request.user

    try:
        instance = meeting.edit_requests.get(participant=user)
    except EditRequest.DoesNotExist:
        instance = EditRequest.objects.create(
            meeting=meeting, participant=user, content=""
        )

    form = RequestEditForm(
        request.POST or None,
        instance=instance,
        initial={"meeting": meeting, "participant": user},
    )

    if form.is_valid():
        form.save()
        return redirect("meeting-detail", id)
    else:
        form = RequestEditForm(
            instance=instance,
            initial={"meeting": meeting, "participant": user},
        )

    context = {"form": form}

    return render(request, "meetings/edit_request.html", context)


# 編輯報告事項
@login_required(login_url="login")
@permission_required("meetings.change_announcement", raise_exception=True)
def edit_announcement_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Meeting.DoesNotExist:
        return redirect("meeting-not-found")

    formset = AnnouncementFormSet(request.POST or None, instance=meeting)
    helper = BaseFormHelper()
    helper.form_id = "edit-announcement-form"
    helper.form_tag = False
    helper.layout = Layout(Field("content"), Field("DELETE"))
    # helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))

    if formset.is_valid():
        formset.save()
        return redirect("edit-announcements", id)
    else:
        formset = AnnouncementFormSet(instance=meeting)

    context = {"formset": formset, "helper": helper, "meeting": meeting}
    return render(request, "meetings/edit_announcement.html", context)


# 編輯討論事項
@login_required(login_url="login")
@permission_required("meetings.change_discussion", raise_exception=True)
def edit_discussion_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Meeting.DoesNotExist:
        return redirect("meeting-not-found")

    formset = DiscussionFormSet(request.POST or None, instance=meeting)
    helper = BaseFormHelper()
    helper.form_id = "edit-discussion-form"
    helper.form_tag = False
    helper.layout = Layout(
        Field("topic"),
        Field("description"),
        Field("resolution"),
        Field("DELETE"),
    )

    if formset.is_valid():
        formset.save()
        return redirect("edit-discussions", id)
    else:
        formset = DiscussionFormSet(instance=meeting)

    context = {"formset": formset, "helper": helper, "meeting": meeting}
    return render(request, "meetings/edit_discussion.html", context)


# 編輯附件
@login_required(login_url="login")
@permission_required("meetings.change_appendix", raise_exception=True)
def edit_appendix_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Meeting.DoesNotExist:
        return redirect("meeting-not-found")

    formset = AppendixFormSet(
        request.POST or None,
        request.FILES or None,
        instance=meeting,
        initial=[{"provider": request.user.get_full_name()}],
    )
    helper = BaseFormHelper()
    helper.form_id = "edit-appendix-form"
    helper.form_tag = False
    helper.layout = Layout(
        Field("provider"),
        Field("file"),
        Field("DELETE"),
    )

    if formset.is_valid():
        formset.save()
        return redirect("edit-appendices", id)
    else:
        formset = AppendixFormSet(
            instance=meeting, initial=[{"provider": request.user.get_full_name()}]
        )

    context = {"formset": formset, "helper": helper, "meeting": meeting}
    return render(request, "meetings/edit_appendix.html", context)


# 寄出開會結果
def send_resolution_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Meeting.DoesNotExist:
        return redirect("meeting-not-found")

    meeting.send_meeting_resolution()

    return render(request, "meetings/send_success.html", {})
