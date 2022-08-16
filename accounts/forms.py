from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UsernameField,
    AuthenticationForm,
)
from crispy_forms.layout import Layout, Field, Submit, Div
from utils.choices import SEX, IDENTITY
from utils.base_form_helper import BaseFormHelper
from .models import *


# 申請帳號的表單
class SignUpForm(UserCreationForm):
    username = forms.CharField(label="使用者名稱", max_length=150, required=True)
    first_name = forms.CharField(label="名稱", max_length=10, required=True)
    last_name = forms.CharField(label="姓氏", max_length=10, required=True)
    password1 = forms.CharField(
        label="密碼",
        max_length=200,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "type": "password"},
        ),
    )
    password2 = forms.CharField(
        label="確認密碼",
        max_length=200,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )
    sex = forms.ChoiceField(label="性別", choices=SEX, required=True, initial=2)
    identity = forms.ChoiceField(label="身分", choices=IDENTITY, required=True, disabled=True)
    email = forms.EmailField(label="電子信箱", required=True)
    phone = forms.CharField(label="連絡電話", max_length=20, required=True)

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
        self.helper = BaseFormHelper()
        self.helper.form_id = "register-form"
        self.helper.layout = Layout(
            Field("username", placeholder="請輸入使用者名稱", css_class="center-field"),
            Field("email", placeholder="請輸入電子信箱", css_class="center-field"),
            Field("password1", placeholder="請輸入密碼", css_class="center-field"),
            Field("password2", placeholder="請再次輸入密碼", css_class="center-field"),
            Field("last_name", placeholder="請輸入姓氏", css_class="center-field"),
            Field("first_name", placeholder="請輸入名稱", css_class="center-field"),
            Field("sex", css_class="center-field"),
            Field("identity", css_class="center-field"),
            Field("phone", placeholder="請輸入連絡電話", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "註冊", css_class="btn-secondary"))

    # def save(self, commit=True):
    #     participant = super().save(commit=commit)
    #     # 根據人員身分加入對應的群組
    #     if participant.identity == 3:
    #         group = Group.objects.get(name="operators")
    #     else:
    #         group = Group.objects.get(name="normal_users")
    #     participant.groups.add(group)
    #     if commit:
    #         participant.save()
    #     return participant


# 基本資料表單
class UserEditFrom(forms.ModelForm):
    last_name = forms.CharField(label="姓氏", max_length=30)
    first_name = forms.CharField(label="名稱", max_length=30)
    email = forms.EmailField(label="電子信箱")
    sex = forms.ChoiceField(label="性別", choices=SEX)
    phone = forms.CharField(label="連絡電話", max_length=10)

    class Meta:
        model = Participant
        fields = ["first_name", "last_name", "email", "sex", "phone"]

    def __init__(self, *args, **kwargs):
        super(UserEditFrom, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "user-edit-form"
        self.helper.layout = Layout(
            Field("last_name", placeholder="請輸入姓氏", css_class="center-field"),
            Field("first_name", placeholder="請輸入名稱", css_class="center-field"),
            Field("email", placeholder="請輸入電子信箱", css_class="center-field"),
            Field("sex", placeholder="請選擇性別", css_class="center-field"),
            Field("phone", placeholder="請輸入連絡電話", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))


# 登入的表單
class LoginForm(AuthenticationForm):
    username = UsernameField(
        # label="使用者名稱",
        label=" ",
        max_length=150,
        required=True,
        error_messages={"required": "帳號或密碼錯誤"},
    )
    password = forms.CharField(
        # label="密碼",
        label=" ",
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
        self.helper = BaseFormHelper()
        self.helper.form_id = "login-form"
        self.helper.layout = Layout(
            Field(
                "username",
                placeholder="請輸入使用者名稱",
                css_class="text-center",  # center-field
            ),
            Field("password", placeholder="請輸入密碼", css_class="text-center"),
            Div(
                Submit("submit", "登入", css_class="btn-secondary"),
                width="100",
                style="text-align:center",
            ),
        )


# 建立業界專家個人資料
class ExpertProfileEditForm(forms.ModelForm):
    company = forms.CharField(label="任職公司", max_length=50, required=True)
    title = forms.CharField(label="職稱", max_length=20, required=True)
    telephone = forms.CharField(label="辦公室電話", max_length=20, required=True)
    address = forms.CharField(label="聯絡地址", max_length=100, required=True)
    bank_account = forms.CharField(label="銀行(郵局)帳號", max_length=14, required=False)

    class Meta:
        model = ExpertProfile
        fields = [
            "company",
            "title",
            "address",
            "telephone",
            "bank_account",
        ]

    def __init__(self, *args, **kwargs):
        super(ExpertProfileEditForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "expert-Edit-form"
        self.helper.layout = Layout(
            Field("company", placeholder="請輸入任職公司", css_class="center-field"),
            Field("title", placeholder="請輸入職稱", css_class="center-field"),
            Field("address", placeholder="請輸入聯絡地址", css_class="center-field"),
            Field("telephone", placeholder="請輸入辦公室電話", css_class="center-field"),
            Field("bank_account", placeholder="請輸入銀行(郵局)帳號", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))


# 建立學生代表個人資料
class StudentProfileEditForm(forms.ModelForm):
    student_id = forms.CharField(label="學號", max_length=15, required=True)
    school_system = forms.CharField(
        label="學制",
        max_length=10,
        required=True,
    )
    grade = forms.CharField(label="年級", max_length=10, required=True)

    class Meta:
        model = StudentProfile
        fields = [
            "student_id",
            "school_system",
            "grade",
        ]

    def __init__(self, *args, **kwargs):
        super(StudentProfileEditForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.layout = Layout(
            Field("student_id", placeholder="請輸入學號", css_class="center-field"),
            Field("school_system", placeholder="請輸入學制", css_class="center-field"),
            Field("grade", placeholder="請輸入年級", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))


# 建立校外老師個人資料
class TeacherProfileEditForm(forms.ModelForm):
    school = forms.CharField(label="任職學校", max_length=50, required=True)
    department = forms.CharField(label="系所", max_length=20, required=True)
    title = forms.CharField(label="職稱", max_length=20, required=True)
    telephone = forms.CharField(label="辦公室電話", max_length=20, required=True)
    address = forms.CharField(label="聯絡地址", max_length=100, required=True)
    bank_account = forms.CharField(label="銀行(郵局)帳號", max_length=14, required=False)

    class Meta:
        model = TeacherProfile
        fields = [
            "school",
            "department",
            "title",
            "telephone",
            "address",
            "bank_account",
        ]

    def __init__(self, *args, **kwargs):
        super(TeacherProfileEditForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "teacher-Edit-form"
        self.helper.layout = Layout(
            Field("school", placeholder="請輸入任職學校", css_class="center-field"),
            Field("department", placeholder="請輸入系所", css_class="center-field"),
            Field("title", placeholder="請輸入職稱", css_class="center-field"),
            Field("telephone", placeholder="請輸入辦公室電話", css_class="center-field"),
            Field("address", placeholder="請輸入聯絡地址", css_class="center-field"),
            Field("bank_account", placeholder="請輸入銀行(郵局)帳號", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))


# 建立系助理個人資料
class AssistantProfileEditForm(forms.ModelForm):
    telephone = forms.CharField(label="辦公室電話", max_length=20, required=True)

    class Meta:
        model = AssistantProfile
        fields = [
            "telephone",
        ]

    def __init__(self, *args, **kwargs):
        super(AssistantProfileEditForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "assistant-Edit-form"
        self.helper.layout = Layout(
            Field("telephone", placeholder="請輸入辦公室電話", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))


# 建立系上老師個人資料
class ProfessorProfileEditForm(forms.ModelForm):
    title = forms.CharField(label="職級", max_length=20, required=True)
    telephone = forms.CharField(label="辦公室電話", max_length=20, required=True)

    class Meta:
        model = ProfessorProfile
        fields = [
            "title",
            "telephone",
        ]

    def __init__(self, *args, **kwargs):
        super(ProfessorProfileEditForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "professor-create-form"
        self.helper.layout = Layout(
            Field("title", placeholder="請輸入職級", css_class="center-field"),
            Field("telephone", placeholder="請輸入辦公室電話", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))


# 根據identity決定要回傳的表單
def get_edit_form(method, user):
    identity = user.identity
    if identity == 0:
        return ExpertProfileEditForm(method, instance=user.expert_profile)
    elif identity == 1:
        return StudentProfileEditForm(method, instance=user.student_profile)
    elif identity == 2:
        return TeacherProfileEditForm(method, instance=user.teacher_profile)
    elif identity == 3:
        return AssistantProfileEditForm(method, instance=user.assistant_profile)
    else:
        return ProfessorProfileEditForm(method, instance=user.professor_profile)
