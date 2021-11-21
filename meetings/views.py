from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Meeting

# from .forms import MeetingCreateForm


# 首頁(會呈現近期的會議)
class MeetingListView(ListView):
    model = Meeting
    template_name = "index.html"


# 會議細節(議程)
class MeetingDetailView(DetailView):
    model = Meeting
    template_name = "meetings/meeting_detail.html"


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
