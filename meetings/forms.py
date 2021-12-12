from django import forms
from .models import *
from accounts.models import Participant
from accounts.forms import BaseFormHelper
from crispy_forms.helper import Layout
from crispy_forms.layout import Submit, Field
from crispy_forms.bootstrap import InlineCheckboxes


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, member):
        return member.last_name + member.first_name


class BaseFormSetHelper(BaseFormHelper):
    def __init__(self, *args, **kwargs):
        super(BaseFormSetHelper, self).__init__(*args, **kwargs)
        self.form_class = "form-vertical"
        self.label_class = "col-sm-12 col-md-12 col-lg-12"
        self.field_class = "col-sm-12 col-md-12 col-lg-12"
        self.add_input(Submit("submit", "保存", css_class="btn-secondary"))


# 建立會議的表單
class MeetingCreateForm(forms.ModelForm):
    name = forms.CharField(label="會議名稱", max_length=100, required=True)
    type = forms.CharField(label="種類", max_length=20, required=True)
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
    participants = CustomModelMultipleChoiceField(
        label="與會人員",
        queryset=Participant.objects.all(),
        widget=forms.CheckboxSelectMultiple,
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
        super(MeetingCreateForm, self).__init__(*args, **kwargs)
        # 將html的datetime-local轉成datetime field
        self.fields["date"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.helper = BaseFormHelper()
        self.helper.form_id = "meeting-create-form"
        # 共通欄位
        self.helper.layout = Layout(
            Field("name"),
            Field("type"),
            Field("date"),
            Field("location"),
            Field("chairman"),
            Field("minutes_taker"),
            InlineCheckboxes("participants"),
            Field("speech"),
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
    type = forms.CharField(label="種類", max_length=20, required=False)
    date = forms.DateField(
        label="時間",
        widget=forms.DateInput(
            attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
        ),
        required=False,
    )
    location = forms.CharField(label="地點", max_length=100, required=False)
    chairman = forms.CharField(label="主席", max_length=20, required=False)
    minutes_taker = forms.CharField(label="記錄人員", max_length=20, required=False)
    participants = CustomModelMultipleChoiceField(
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
            Field("name"),
            Field("type"),
            Field("date"),
            Field("location"),
            Field("chairman"),
            Field("minutes_taker"),
            InlineCheckboxes("participants"),
            Field("speech"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))


# 編輯出席紀錄的表單
class AttendanceEditForm(forms.ModelForm):
    # participant是modelchoicefield -> 可以修正了
    class Meta:
        model = Attendance
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AttendanceEditForm, self).__init__(*args, **kwargs)
        # 將participant變成唯讀
        self.fields["participant"].widget.attrs["disabled"] = "disabled"


# 將AttendatnceEditForm轉換成InlineFormset
AttendanceFormSet = forms.inlineformset_factory(
    Meeting, Attendance, form=AttendanceEditForm, extra=0
)
