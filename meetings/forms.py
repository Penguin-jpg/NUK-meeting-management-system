from django import forms
from .models import Meeting
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Field


class MeetingCreateForm(forms.ModelForm):
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

    class Meta:
        model = Meeting
        fields = [
            "name",
            "type",
            "date",
            "location",
            "chairman",
            "minutes_taker",
        ]

    def __init__(self, *args, **kwargs):
        super(MeetingCreateForm, self).__init__(*args, **kwargs)
        # 將html的datetime-local轉成datetime field
        self.fields["date"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "blueForms"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-12 col-md-4 col-lg-2"
        self.helper.field_class = "col-sm-12 col-md-6 col-lg-8"
        self.helper.form_id = "edit-meeting-form"
        # 共通欄位
        self.helper.layout = Layout(
            Field("name"),
            Field("type"),
            Field("date"),
            Field("location"),
            Field("chairman"),
            Field("minutes_taker"),
        )
        self.helper.add_input(Submit("submit", "建立", css_class="btn-secondary"))


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

    class Meta:
        model = Meeting
        fields = [
            "name",
            "type",
            "date",
            "location",
            "chairman",
            "minutes_taker",
        ]

    def __init__(self, *args, **kwargs):
        super(MeetingEditForm, self).__init__(*args, **kwargs)
        self.fields["date"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "blueForms"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-12 col-md-4 col-lg-2"
        self.helper.field_class = "col-sm-12 col-md-6 col-lg-8"
        self.helper.form_id = "edit-meeting-form"
        # 共通欄位
        self.helper.layout = Layout(
            Field("name"),
            Field("type"),
            Field("date"),
            Field("location"),
            Field("chairman"),
            Field("minutes_taker"),
        )
        self.helper.add_input(Submit("submit", "修改", css_class="btn-secondary"))
