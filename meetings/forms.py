from django import forms
from .models import *
from accounts.models import Participant
from accounts.forms import BaseFormHelper
from crispy_forms.helper import Layout
from crispy_forms.layout import Submit, Field, Div
from crispy_forms.bootstrap import InlineCheckboxes

# InlineCheckboxes.template = "meetings/mycheckboxselectmultiple.html"


TYPE = ((0, "系務會議"), (1, "系教評會"), (2, "系課程委員會"), (3, "招生暨學生事務委員會"), (4, "系發展委員會"))


# 建立會議的表單
class MeetingCreateForm(forms.ModelForm):
    name = forms.CharField(label="會議名稱", max_length=100, required=True)
    type = forms.ChoiceField(label="種類", choices=TYPE, required=True)
    date = forms.DateTimeField(
        label="時間",
        widget=forms.DateInput(
            attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
        ),
        required=True,
    )
    location = forms.CharField(label="地點", max_length=100, required=True)
    chairman = forms.CharField(label="主席", max_length=20, required=True)
    minutes_taker = forms.CharField(label="記錄人員", max_length=20, required=True)
    participants = forms.ModelMultipleChoiceField(
        label="與會人員",
        queryset=Participant.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
    )
    speech = forms.CharField(label="主席致詞", max_length=500, initial="略", required=False)

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
            Field("name", css_class="center-field"),
            Field("type", css_class="center-field"),
            Field("date", css_class="center-field"),
            Field("location", css_class="center-field"),
            Field("chairman", css_class="center-field"),
            Field("minutes_taker", css_class="center-field"),
            InlineCheckboxes("participants", css_class="checkboxes-field"),
            Field("speech", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "建立", css_class="btn-secondary"))

    def save(self, commit=True):
        meeting = super().save(commit=commit)
        participants = self.cleaned_data["participants"]
        # 將出席紀錄加入該會議
        for participant in participants:
            Attendance.objects.create(meeting=meeting, participant=participant)
        if commit:
            meeting.save()
        return meeting


# 編輯會議的表單
class MeetingEditForm(forms.ModelForm):
    name = forms.CharField(label="會議名稱", max_length=100, required=False)
    type = forms.ChoiceField(label="種類", choices=TYPE, required=False)
    date = forms.DateTimeField(
        label="時間",
        widget=forms.DateInput(
            attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
        ),
        required=False,
    )
    location = forms.CharField(label="地點", max_length=100, required=False)
    chairman = forms.CharField(label="主席", max_length=20, required=False)
    minutes_taker = forms.CharField(label="記錄人員", max_length=20, required=False)
    participants = forms.ModelMultipleChoiceField(
        label="與會人員",
        queryset=Participant.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    speech = forms.CharField(label="主席致詞", max_length=500, required=False)

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
            Field("name", css_class="center-field"),
            Field("type", css_class="center-field"),
            Field("date", css_class="center-field"),
            Field("location", css_class="center-field"),
            Field("chairman", css_class="center-field"),
            Field("minutes_taker", css_class="center-field"),
            InlineCheckboxes("participants"),
            Field("speech", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))

    def save(self, commit=True):
        meeting = super().save(commit=commit)
        participants = self.cleaned_data["participants"]

        for participant in participants:
            # 如果找不到該與會人員的出席紀錄就新增
            if not Attendance.objects.filter(meeting=meeting, participant=participant):
                Attendance.objects.create(meeting=meeting, participant=participant)
        if commit:
            meeting.save()
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


# 將AttendatnceEditForm轉換成InlineFormset
AttendanceFormSet = forms.inlineformset_factory(
    Meeting, Attendance, form=AttendanceEditForm, extra=0
)

# 建立臨時動議的表單
class ExtemporeMotionCreateForm(forms.ModelForm):
    meeting = forms.ModelChoiceField(
        queryset=Meeting.objects.all(), label="會議名稱", disabled=True, required=False
    )
    proposer = forms.CharField(label="提案人", max_length=20, required=True)
    content = forms.CharField(label="內容", max_length=500, required=True)

    class Meta:
        model = ExtemporeMotion
        fields = ["meeting", "proposer", "content"]

    def __init__(self, *args, **kwargs):
        super(ExtemporeMotionCreateForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "create-extemporeMotion-form"
        # 共通欄位
        self.helper.layout = Layout(
            Field("meeting", css_class="center-field"),
            Field("proposer", css_class="center-field"),
            Field("content", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "建立", css_class="btn-secondary"))


# 編輯臨時動議的表單
class ExtemporeMotionEditForm(forms.ModelForm):
    meeting = forms.ModelChoiceField(
        queryset=Meeting.objects.all(), label="會議名稱", disabled=True, required=False
    )
    proposer = forms.CharField(label="提案人", max_length=20, required=True)
    content = forms.CharField(label="內容", max_length=500, required=True)

    class Meta:
        model = ExtemporeMotion
        fields = ["meeting", "proposer", "content"]


# 將 ExtemporeMotionEditForm 轉換成 inlineFormset
ExtemporeMotionFormSet = forms.inlineformset_factory(
    Meeting, ExtemporeMotion, form=ExtemporeMotionEditForm, extra=0
)

# 建立報告事項的表單
class AnnouncementCreateForm(forms.ModelForm):
    meeting = forms.ModelChoiceField(
        queryset=Meeting.objects.all(), label="會議名稱", disabled=True, required=False
    )
    content = forms.CharField(label="內容", max_length=500, required=True)

    class Meta:
        model = Announcement
        fields = ["meeting", "content"]

    def __init__(self, *args, **kwargs):
        super(AnnouncementCreateForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "create-announcement-form"
        # 共通欄位
        self.helper.layout = Layout(
            Field("meeting", css_class="center-field"),
            Field("content", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "建立", css_class="btn-secondary"))


# 編輯報告事項的表單
class AnnouncementEditForm(forms.ModelForm):
    meeting = forms.ModelChoiceField(
        queryset=Meeting.objects.all(), label="會議名稱", disabled=True, required=False
    )
    content = forms.CharField(label="內容", max_length=500, required=True)

    class Meta:
        model = Announcement
        fields = ["meeting", "content"]


# 將 AnnouncementEditForm 轉換成 inlineFormset
AnnouncementFormSet = forms.inlineformset_factory(
    Meeting, Announcement, form=AnnouncementEditForm, extra=0
)

# 建立討論事項的表單
class DiscussionCreateForm(forms.ModelForm):
    meeting = forms.ModelChoiceField(
        queryset=Meeting.objects.all(), label="會議名稱", disabled=True, required=False
    )
    topic = forms.CharField(label="案由", max_length=25, required=True)
    description = forms.CharField(label="說明", max_length=500, required=True)
    resolution = forms.CharField(label="決議", max_length=150, required=True)

    class Meta:
        model = Discussion
        fields = ["meeting", "topic", "description", "resolution"]

    def __init__(self, *args, **kwargs):
        super(DiscussionCreateForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "create-discussion-form"
        # 共通欄位
        self.helper.layout = Layout(
            Field("meeting", css_class="center-field"),
            Field("topic", css_class="center-field"),
            Field("description", css_class="center-field"),
            Field("resolution", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "建立", css_class="btn-secondary"))


# 編輯討論事項的表單
class DiscussionEditForm(forms.ModelForm):
    meeting = forms.ModelChoiceField(
        queryset=Meeting.objects.all(), label="會議名稱", disabled=True, required=False
    )
    topic = forms.CharField(label="案由", max_length=25, required=True)
    description = forms.CharField(label="說明", max_length=500, required=True)
    resolution = forms.CharField(label="決議", max_length=150, required=True)

    class Meta:
        model = Discussion
        fields = ["meeting", "topic", "description", "resolution"]


# 將 DiscussionEditForm 轉換成 inlineFormset
DiscussionFormSet = forms.inlineformset_factory(
    Meeting, Discussion, form=DiscussionEditForm, extra=1
)
