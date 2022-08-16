from msilib.schema import Font
from django import forms
from .models import *
from accounts.models import Participant
from crispy_forms.helper import Layout
from crispy_forms.layout import Submit, Field
from crispy_forms.bootstrap import InlineCheckboxes
from utils.choices import MEETING_TYPES
from utils.base_form_helper import BaseFormHelper

# 使用自訂的template，不然field_class會被蓋掉
# InlineCheckboxes.template = "meetings/custom_checkboxselectmultiple_inline.html"


# 建立會議的表單
class MeetingCreateForm(forms.ModelForm):
    name = forms.CharField(label="會議名稱", max_length=100, required=True)
    type = forms.ChoiceField(label="種類", choices=MEETING_TYPES, required=True)
    date = forms.DateTimeField(
        label="時間",
        widget=forms.DateInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        required=True,
    )
    location = forms.CharField(label="地點", max_length=100, required=True)
    chairman = forms.ModelChoiceField(queryset=Participant.objects.all(), label="主席", required=True)
    minutes_taker = forms.ModelChoiceField(queryset=Participant.objects.all(), label="記錄人員", required=True)
    participants = forms.ModelMultipleChoiceField(
        label="與會人員",
        queryset=Participant.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
    )
    speech = forms.CharField(
        label="主席致詞",
        max_length=500,
        initial="略",
        widget=forms.Textarea(attrs={"rows": 5}),
        required=False,
    )

    class Meta:
        model = Meeting
        fields = [
            "name",
            "type",
            "date",
            "location",
            "chairman",
            "minutes_taker",
            "participants",
            "speech",
        ]

    def __init__(self, *args, **kwargs):
        super(MeetingCreateForm, self).__init__(*args, **kwargs)
        # 將html的datetime-local轉成datetime field
        self.fields["date"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.helper = BaseFormHelper()
        self.helper.form_id = "meeting-create-form"

        # 共通欄位
        self.helper.layout = Layout(
            Field("name", placeholder="請輸入會議名稱", css_class="center-field"),
            Field("type", css_class="center-field"),
            Field("date", css_class="center-field"),
            Field("location", placeholder="請輸入會議地點", css_class="center-field"),
            Field("chairman", css_class="center-field"),
            Field("minutes_taker", css_class="center-field"),
            InlineCheckboxes("participants"),
            Field("speech", placeholder="請輸入主席致詞", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "建立", css_class="btn-secondary"))

    def save(self, commit=True):
        meeting = super().save(commit=commit)
        participants = meeting.participants

        # 將主席和紀錄人員加入與會人員
        participants.add(meeting.chairman)
        participants.add(meeting.minutes_taker)

        # 建立出席紀錄
        for participant in participants.all():
            Attendance.objects.create(meeting=meeting, participant=participant)

        if commit:
            meeting.save()
            # meeting.send_meeting_notification()
        return meeting


# 編輯會議的表單
class MeetingEditForm(forms.ModelForm):
    name = forms.CharField(label="會議名稱", max_length=200, required=False)
    type = forms.ChoiceField(label="種類", choices=MEETING_TYPES, required=False)
    date = forms.DateTimeField(
        label="時間",
        widget=forms.DateInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        required=False,
    )
    location = forms.CharField(label="地點", max_length=100, required=False)
    chairman = forms.ModelChoiceField(queryset=Participant.objects.all(), label="主席", required=False)
    minutes_taker = forms.ModelChoiceField(queryset=Participant.objects.all(), label="記錄人員", required=False)
    participants = forms.ModelMultipleChoiceField(
        label="與會人員",
        queryset=Participant.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    speech = forms.CharField(
        label="主席致詞",
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 5}),
        required=False,
    )

    class Meta:
        model = Meeting
        fields = [
            "name",
            "type",
            "date",
            "location",
            "chairman",
            "minutes_taker",
            "participants",
            "speech",
        ]

    def __init__(self, *args, **kwargs):
        super(MeetingEditForm, self).__init__(*args, **kwargs)
        self.fields["date"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.helper = BaseFormHelper()
        self.helper.form_id = "edit-meeting-form"
        # 共通欄位
        self.helper.layout = Layout(
            Field("name", placeholder="請輸入會議名稱", css_class="center-field"),
            Field("type", css_class="center-field"),
            Field("date", css_class="center-field"),
            Field("location", placeholder="請輸入會議地點", css_class="center-field"),
            Field("chairman", css_class="center-field"),
            Field("minutes_taker", css_class="center-field"),
            InlineCheckboxes("participants"),
            Field("speech", placeholder="請輸入主席致詞", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))

    def save(self, commit=True):
        meeting = super().save(commit=commit)
        participants = meeting.participants

        # 將主席和紀錄人員加入與會人員
        participants.add(meeting.chairman)
        participants.add(meeting.minutes_taker)

        if commit:
            meeting.save()
            # meeting.send_meeting_notification()
        return meeting


# 編輯出席紀錄的表單
class AttendanceEditForm(forms.ModelForm):
    participant = forms.ModelChoiceField(
        Participant.objects.all(),
        label="與會人員",
        disabled=True,
        required=False,
    )
    attend = forms.BooleanField(label="出席", required=False)

    class Meta:
        model = Attendance
        fields = [
            "participant",
            "attend",
        ]


# 編輯修改請求的表單
class RequestEditForm(forms.ModelForm):
    meeting = forms.ModelChoiceField(
        Meeting.objects.all(),
        label="會議",
        disabled=True,
        required=True,
    )
    participant = forms.ModelChoiceField(
        Participant.objects.all(),
        label="與會人員",
        disabled=True,
        required=True,
    )
    content = forms.CharField(
        label="內容",
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 5}),
        required=True,
    )

    class Meta:
        model = EditRequest
        fields = [
            "meeting",
            "participant",
            "content",
        ]

    def __init__(self, *args, **kwargs):
        super(RequestEditForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "edit-request-form"
        # 共通欄位
        self.helper.layout = Layout(
            Field("participant"),
            Field("content", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))


# 編輯報告事項的表單
class AnnouncementEditForm(forms.ModelForm):
    meeting = forms.ModelChoiceField(queryset=Meeting.objects.all(), label="會議名稱", disabled=True, required=True)
    content = forms.CharField(
        label="內容",
        max_length=500,
        required=True,
        widget=forms.Textarea(attrs={"rows": 8, "cols": 40}),
    )

    class Meta:
        model = Announcement
        fields = ["meeting", "content"]


# 編輯討論事項的表單
class DiscussionEditForm(forms.ModelForm):
    meeting = forms.ModelChoiceField(queryset=Meeting.objects.all(), label="會議名稱", disabled=True, required=True)
    topic = forms.CharField(label="案由", max_length=25, required=True)
    description = forms.CharField(
        label="說明",
        max_length=500,
        required=True,
        widget=forms.Textarea(attrs={"rows": 8, "cols": 40}),
    )
    resolution = forms.CharField(
        label="決議",
        initial="無",
        max_length=150,
        required=False,
        widget=forms.Textarea(attrs={"rows": 5, "cols": 40}),
    )

    class Meta:
        model = Discussion
        fields = ["meeting", "topic", "description", "resolution"]


# 編輯附件的表單
class AppendixEditForm(forms.ModelForm):
    meeting = forms.ModelChoiceField(queryset=Meeting.objects.all(), label="會議名稱", disabled=True, required=True)
    provider = forms.CharField(label="提供者", max_length=20, required=True)
    file = forms.FileField(label="檔案", required=True)

    class Meta:
        model = Appendix
        fields = ["meeting", "provider", "file"]


# 編輯會議建議的表單
class AdviceEditForm(forms.ModelForm):
    meeting = forms.ModelChoiceField(
        Meeting.objects.all(),
        label="會議",
        disabled=True,
        required=True,
    )
    participant = forms.ModelChoiceField(
        Participant.objects.all(),
        label="與會人員",
        disabled=True,
        required=True,
    )
    advice = forms.CharField(
        label="建議",
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 5}),
        required=True,
    )

    class Meta:
        model = Advice
        fields = [
            "meeting",
            "participant",
            "advice",
        ]

    def __init__(self, *args, **kwargs):
        super(AdviceEditForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "edit-advice-form"
        # 共通欄位
        self.helper.layout = Layout(
            Field("participant"),
            Field("advice", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))
