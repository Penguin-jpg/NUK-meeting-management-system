from django.contrib.auth.forms import (
    PasswordChangeForm,
    UserCreationForm,
    UserChangeForm,
)
from django.contrib.auth.models import User
from django import forms
from .models import Participant
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Div, Row, Column, Field

SEX = ((0, "男性"), (1, "女性"))
IDENTITY = ((0, "業界專家"), (1, "學生代表"), (2, "校外老師"), (3, "系助理"), (4, "系上老師"))

# 申請帳號的表格
class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = (
        forms.CharField(
            max_length=10,
        ),
    )
    last_name = (
        forms.CharField(
            max_length=10,
        ),
    )
    sex = forms.ChoiceField(choices=SEX, required=False)
    identity = forms.ChoiceField(choices=IDENTITY, required=False)
    email = email = forms.EmailField(required=False)
    phone = PhoneNumberField(region="TW", required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "sex",
            "identity",
            "phone",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "使用者名稱"
        self.fields["first_name"].label = "姓氏"
        self.fields["last_name"].label = "名稱"
        self.fields["sex"].label = "性別"
        self.fields["identity"].label = "身分"
        self.fields["phone"].label = "連絡電話"
        self.fields["password1"].label = "密碼"
        self.fields["password2"].label = "請重新輸入密碼"
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "blueForms"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-8"
        self.helper.form_id = "register-form"
        self.helper.layout = Layout(
            Field("username"),
            Field("email"),
            Field("password1"),
            Field("password2"),
            Field("first_name"),
            Field("last_name"),
            Field("sex"),
            Field("identity"),
            Field("phone"),
        )
        self.helper.add_input(
            Submit("submit", "註冊", css_class="btn-secondary float: right")
        )
