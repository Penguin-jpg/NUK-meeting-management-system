from django import forms
from django.contrib.auth.forms import (
    PasswordChangeForm,
    UserCreationForm,
    UserChangeForm,
    UsernameField,
    AuthenticationForm,
)
from .models import Participant
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import HTML, Submit, Div, Row, Column, Field, HTML

SEX = ((0, "女性"), (1, "男性"))
IDENTITY = (
    ("empty", ""),
    ("expert", "業界專家"),
    ("student_presentative", "學生代表"),
    ("external_teacher", "校外老師"),
    ("assistant", "系助理"),
    ("professor", "系上老師"),
)

# 申請帳號的表單
class SignUpForm(UserCreationForm):
    username = forms.CharField(label="使用者名稱", max_length=150, required=True)
    first_name = forms.CharField(label="名稱", max_length=10, required=True)
    last_name = forms.CharField(label="姓氏", max_length=10, required=True)
    password1 = forms.CharField(
        label="密碼",
        max_length=200,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )
    password2 = forms.CharField(
        label="確認密碼",
        max_length=200,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )
    sex = forms.ChoiceField(label="性別", choices=SEX, required=False)
    identity = forms.ChoiceField(label="身分", choices=IDENTITY, required=False)
    email = forms.EmailField(label="電子信箱", required=True)
    phone = PhoneNumberField(label="連絡電話", region="TW", required=False)

    class Meta:
        model = Participant
        fields = [
            "username",
            "last_name",
            "first_name",
            "email",
            "sex",
            "identity",
            "phone",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "blueForms"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-12 col-md-4 col-lg-2"
        self.helper.field_class = "col-sm-12 col-md-6 col-lg-8"
        self.helper.form_id = "register-form"
        self.helper.layout = Layout(
            Field("username"),
            Field("email"),
            Field("password1"),
            HTML(
                """
            <ul class="list" style="list-style-type:none; text-align:left">
                <li><span>- 密碼不能和使用者名稱過度相似</span></li>
                <li><span>- 密碼長度至少要 8 個字元</span></li>
                <li><span>- 不能使用極為常見的密碼</span></li>
                <li><span>- 密碼不能只包含數字</span><li>
            </ul>"""
            ),
            Field("password2"),
            Field("last_name"),
            Field("first_name"),
            Field("sex"),
            Field("identity"),
            Field("phone"),
        )
        self.helper.add_input(Submit("submit", "註冊", css_class="btn-secondary"))


# 登入的表單
class LoginForm(AuthenticationForm):
    username = UsernameField(label="使用者名稱", max_length=150, required=True)
    password = forms.CharField(
        label="密碼",
        max_length=200,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )

    class Meta:
        model = Participant
        fields = [
            "username",
            "password",
        ]

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "blueForms"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-12 col-md-4 col-lg-2"
        self.helper.field_class = "col-sm-12 col-md-6 col-lg-8"
        self.helper.form_id = "login-form"
        self.helper.layout = Layout(
            Field("username"),
            Field("password"),
        )
        self.helper.add_input(Submit("submit", "登入", css_class="btn-secondary"))


class ParticipantChangeForm(UserChangeForm):
    username = forms.CharField(label="使用者名稱", max_length=150, required=True)
    first_name = forms.CharField(label="名稱", max_length=10, required=True)
    last_name = forms.CharField(label="姓氏", max_length=10, required=True)
    sex = forms.ChoiceField(label="性別", choices=SEX, required=False)
    identity = forms.ChoiceField(label="身分", choices=IDENTITY, required=False)
    email = forms.EmailField(label="電子信箱", required=True)
    phone = PhoneNumberField(label="連絡電話", region="TW", required=False)

    class Meta:
        model = Participant
        fields = [
            "username",
            "last_name",
            "first_name",
            "password",
            "email",
            "sex",
            "identity",
            "phone",
        ]

    def __init__(self, *args, **kwargs):
        super(ParticipantChangeForm, self).__init__(*args, **kwargs)
        self.fields["password"].label = "密碼"
