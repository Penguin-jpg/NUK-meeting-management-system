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

SEX = ((0, "女性"), (1, "男性"))

# 申請帳號的表格
class SignUpForm(UserCreationForm):
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
    sex = forms.ChoiceField(choices=SEX)
    identity = forms.CharField(
        max_length=50,
        label="身分",
    )
    email = email = forms.EmailField()
    phone = PhoneNumberField(region="TW")

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
        self.helper.form_method = "POST"
        self.helper.form_class = "blueForms"
        self.helper.form_id = "register-form"
        self.helper.layout = Layout(
            Row(
                Column("username", css_class="col-6"),
                Column("email", css_class="col-6"),
            ),
            Row(
                Column("first_name", css_class="col-6"),
                Column("last_name", css_class="col-6"),
            ),
            Row(
                Column("password1", css_class="col-6"),
                Column("password2", css_class="col-6"),
            ),
        )
        # self.helper.add_input(Submit("submit", "註冊", css_class="btn-primary"))
        self.helper.add_input(Submit("submit", "Submit"))
