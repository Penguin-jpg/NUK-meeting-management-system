from django import forms
from meetings.models import Meeting, Attendance, Announcement, Discussion, Appendix
from meetings.forms import (
    AttendanceEditForm,
    AnnouncementEditForm,
    DiscussionEditForm,
    AppendixEditForm,
)

# 將AttendatnceEditForm轉換成InlineFormset
AttendanceFormSet = forms.inlineformset_factory(
    Meeting, Attendance, form=AttendanceEditForm, extra=0
)

# 將 AnnouncementEditForm 轉換成 inlineFormset
AnnouncementFormSet = forms.inlineformset_factory(
    Meeting,
    Announcement,
    form=AnnouncementEditForm,
    extra=1,
    can_delete=True,
    can_delete_extra=False,
)

# 將 DiscussionEditForm 轉換成 inlineFormset
DiscussionFormSet = forms.inlineformset_factory(
    Meeting,
    Discussion,
    form=DiscussionEditForm,
    extra=1,
    can_delete=True,
    can_delete_extra=False,
)

# 將 AppendixEditForm 轉換成 inlineFormset
AppendixFormSet = forms.inlineformset_factory(
    Meeting,
    Appendix,
    form=AppendixEditForm,
    extra=1,
    can_delete=True,
    can_delete_extra=False,
)
