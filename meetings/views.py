from django.shortcuts import render, get_object_or_404, redirect
from .models import Meeting

# from .forms import MeetingCreateForm


# 首頁(會呈現近期的會議)
def meeting_list_view(request):
    queryset = Meeting.objects.all()
    context = {"meetings": queryset}
    return render(request, "index.html", context)


# 會議細節(議程)
def meeting_detail_view(request, id):
    meeting = get_object_or_404(Meeting, id=id)  # 暫時使用id當作查詢，之後會改成用uuid
    Meeting.ob
    context = {"meeting": meeting}
    return render(request, "meeting/meeting_detail.html", context)


# 建立會議
# def meeting_create_view(request):
#     form = MeetingCreateForm()
#     if form.is_valid():
#         form.save()
#         return redirect("home")
#     else:
#         form = MeetingCreateForm()
#     context = {
#         "form": form,
#     }
#     return render(request, "meeting/meeting_create.html", context)
