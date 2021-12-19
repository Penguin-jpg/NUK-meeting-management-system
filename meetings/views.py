from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from .models import *
from .forms import (
    MeetingCreateForm,
    MeetingEditForm,
    ExtemporeMotionCreateForm,
    ExtemporeMotionEditForm,
    AnnouncementCreateForm,
    AnnouncementEditForm,
    DiscussionCreateForm,
    DiscussionEditForm,
    AttendanceFormSet,
    BaseFormHelper,
    ExtemporeMotionFormSet,
    AnnouncementFormSet,
    DiscussionFormSet,
)
from .utils import Calendar
from datetime import datetime, timedelta
import calendar
from crispy_forms.layout import Layout, Field, Submit

# 取得日期
def get_date(request_day):
    if request_day:
        year, month = (int(x) for x in request_day.split("-"))
        return datetime(year, month, day=1)
    return datetime.now()


# 上個月
def previous_month(date):
    first = date.replace(day=1)
    previous_month = first - timedelta(days=1)
    month = "date=" + str(previous_month.year) + "-" + str(previous_month.month)
    return month


# 下個月
def next_month(date):
    days_in_month = calendar.monthrange(date.year, date.month)[1]
    last = date.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "date=" + str(next_month.year) + "-" + str(next_month.month)
    return month


# 當找不到某個會議時就顯示這個頁面
def meeting_not_found_view(request):
    return render(request, "meetings/meeting_not_found.html", {})


# 首頁(會用日曆紀錄已建立的會議)
def home_view(request):
    date = get_date(request.GET.get("date", None))
    calendar = Calendar(date.year, date.month).formatmonth(withyear=True)

    context = {
        "calendar": calendar,
        "previous_month": previous_month(date),
        "next_month": next_month(date),
    }

    return render(request, "index.html", context)


# 建立會議
@login_required(login_url="login")
# @permission_required("meetings.add_meeting", raise_exception=True)
def meeting_create_view(request):
    form = MeetingCreateForm(request.POST or None)
    if form.is_valid():
        meeting = form.save()
        return redirect("meeting-detail", meeting.id)
    else:
        form = MeetingCreateForm()

    context = {"form": form}

    return render(request, "meetings/meeting_create.html", context)


# 會議列表
@method_decorator(login_required(login_url="login"), name="dispatch")
class MeetingListView(ListView):
    model = Meeting
    template_name = "meetings/meeting_list.html"


# ----------------------------保留------------------------------------------
# 會議細節(議程) 如何呈現
# @method_decorator(login_required(login_url="login"), name="dispatch")
# class MeetingDetailView(DetailView):
#     model = Meeting, ExtemporeMotion, Announcement, Discussion
#     template_name = "meetings/meeting_detail.html"

#     def get_object(self):
#         id = self.kwargs["id"]
#         return get_object_or_404(Meeting, id=id)
# --------------------------------------------------------------------------

# 會議細節(議程)
@login_required(login_url="login")
def meeting_detail_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Meeting.DoesNotExist:
        return redirect("meeting-not-found")
    announcements = meeting.announcement_set.all()
    discussions = meeting.discussion_set.all()
    extempore_motions = meeting.extemporemotion_set.all()

    context = {
        "meeting": meeting,
        "announcements": announcements,
        "discussions": discussions,
        "extempore_motions": extempore_motions,
    }

    return render(request, "meetings/meeting_detail.html", context)


# 編輯會議資料
@login_required(login_url="login")
@permission_required("meetings.change_meeting", raise_exception=True)
def edit_meeting_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Meeting.DoesNotExist:
        return redirect("meeting-not-found")

    form = MeetingEditForm(request.POST or None, instance=meeting)
    if form.is_valid():
        form.save()
        return redirect("meeting-detail", id)
    else:
        form = MeetingEditForm(instance=meeting)

    context = {"form": form, "meeting": meeting}

    return render(request, "meetings/edit_meeting.html", context)


# 刪除會議資料
@login_required(login_url="login")
@permission_required("meetings.delete_meeting", raise_exception=True)
def meeting_delete_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Meeting.DoesNotExist:
        return redirect("meeting-not-found")

    if request.method == "POST":
        meeting.delete()
        return redirect("meeting-list")

    context = {"meeting": meeting}

    return render(request, "meetings/meeting_delete.html", context)


# 顯示某一天的所有會議
@login_required(login_url="login")
def meeting_today_view(request, year, month, day):
    try:
        meetings = Meeting.objects.filter(
            date__year=year, date__month=month, date__day=day
        )
    except Meeting.DoesNotExist:
        return redirect("meeting-not-found")

    context = {
        "meetings": meetings,
    }

    return render(request, "meetings/meeting_today.html", context)


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


# 編輯人員出席紀錄
# https://punchagan.muse-amuse.in/blog/django-modelformset-multiple-saves/
@login_required(login_url="login")
@permission_required("meetings.change_meeting", raise_exception=True)
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
        # print(formset.errors)
        formset = AttendanceFormSet(instance=meeting)

    context = {"formset": formset, "helper": helper}

    return render(request, "meetings/edit_attendance.html", context)


# 若在會議尚未開始時點擊出席名單就顯示這個頁面
def meeting_not_begin_view(request):
    return render(request, "meetings/meeting_not_begin.html", {})


# 建立臨時動議
@login_required(login_url="login")
# @permission_required("meetings.add_meeting", raise_exception=True)
def extemporeMotion_create_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Discussion.DoesNotExist:
        return redirect("discussion-not-found")
    form = ExtemporeMotionCreateForm(request.POST or None, initial={"meeting": meeting})
    if form.is_valid():
        extempore_motion = form.save()
        return redirect("meeting-detail", id)
    else:
        form = ExtemporeMotionCreateForm(initial={"meeting": meeting})

    context = {"form": form}

    return render(request, "meetings/extempore_motion_create.html", context)


# 編輯臨時動議
@login_required(login_url="login")
# @permission_required("meetings.change_meeting", raise_exception=True)
def edit_extempore_motion_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except ExtemporeMotion.DoesNotExist:
        return redirect("discussion-not-found")

    formset = ExtemporeMotionFormSet(request.POST or None, instance=meeting)
    helper = BaseFormHelper()
    helper.form_id = "edit-extemporemotion-form"
    helper.layout = Layout(Field("meeting"), Field("proposer"), Field("content"))
    helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))

    if formset.is_valid():
        formset.save()
        return redirect("meeting-detail", id)
    else:
        formset = ExtemporeMotionFormSet(instance=meeting)

    context = {"formset": formset, "helper": helper}

    return render(request, "meetings/edit_extempore_motion.html", context)


# 建立報告事項
@login_required(login_url="login")
# @permission_required("meetings.add_meeting", raise_exception=True)
def announcement_create_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Discussion.DoesNotExist:
        return redirect("discussion-not-found")
    form = AnnouncementCreateForm(request.POST or None, initial={"meeting": meeting})
    if form.is_valid():
        announcement = form.save()
        return redirect("meeting-detail", id)
    else:
        form = AnnouncementCreateForm(initial={"meeting": meeting})

    context = {"form": form}

    return render(request, "meetings/announcement_create.html", context)


# 編輯報告事項
@login_required(login_url="login")
# @permission_required("meetings.change_meeting", raise_exception=True)
def edit_announcement_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Announcement.DoesNotExist:
        return redirect("discussion-not-found")

    formset = AnnouncementFormSet(request.POST or None, instance=meeting)
    helper = BaseFormHelper()
    helper.form_id = "edit-announcement-form"
    helper.layout = Layout(Field("meeting"), Field("content"))
    helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))

    if formset.is_valid():
        formset.save()
        return redirect("meeting-detail", id)
    else:
        formset = AnnouncementFormSet(instance=meeting)

    context = {"formset": formset, "helper": helper}

    return render(request, "meetings/edit_announcement.html", context)


# 建立討論事項
@login_required(login_url="login")
# @permission_required("meetings.add_meeting", raise_exception=True)
def discussion_create_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Discussion.DoesNotExist:
        return redirect("discussion-not-found")
    form = DiscussionCreateForm(request.POST or None, initial={"meeting": meeting})
    if form.is_valid():
        discussion = form.save()
        return redirect("meeting-detail", id)
    else:
        form = DiscussionCreateForm(initial={"meeting": meeting})

    context = {"form": form}

    return render(request, "meetings/discussion_create.html", context)


# 編輯討論事項
@login_required(login_url="login")
# @permission_required("meetings.change_meeting", raise_exception=True)
def edit_discussion_view(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except Discussion.DoesNotExist:
        return redirect("discussion-not-found")

    formset = DiscussionFormSet(request.POST or None, instance=meeting)
    helper = BaseFormHelper()
    helper.form_id = "edit-discussion-form"
    helper.layout = Layout(
        Field("meeting"),
        Field("topic"),
        Field("description"),
        Field("resolution"),
    )
    helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))

    if formset.is_valid():
        formset.save()
        return redirect("meeting-detail", id)
    else:
        formset = DiscussionFormSet(instance=meeting)

    context = {"formset": formset, "helper": helper}

    return render(request, "meetings/edit_discussion.html", context)
