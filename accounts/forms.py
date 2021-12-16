from django import forms
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
    UsernameField,
    AuthenticationForm,
)
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import *
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import HTML, Hidden, Submit, Field, Div

SEX = ((0, "女性"), (1, "男性"), (2, "其他"))
IDENTITY = (
    (0, "業界專家"),
    (1, "學生代表"),
    (2, "校外老師"),
    (3, "系助理"),
    (4, "系上老師"),
)


class BaseFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(BaseFormHelper, self).__init__(*args, **kwargs)
        self.form_method = "POST"
        self.form_class = "blueForms"
        self.form_class = "form-vertical"
        self.label_class = "col-sm-12 col-md-12 col-lg-12"
        self.field_class = "col-sm-12 offset-md-2 col-md-8 offset-lg-2 col-lg-8"


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
        # help_text="""
        #     <ul style="list-style-type:none; text-align:left">
        #     <li><span class="help-text">- 密碼不能和使用者名稱過度相似</span></li>
        #     <li><span class="help-text">- 密碼長度至少要 8 個字元</span></li>
        #     <li><span class="help-text">- 不能使用極為常見的密碼</span></li>
        #     <li><span class="help-text">- 密碼不能只包含數字</span><li>
        #     </ul>
        #     """,
    )
    password2 = forms.CharField(
        label="確認密碼",
        max_length=200,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )
    identity = forms.ChoiceField(
        label="身分", choices=IDENTITY, required=True, disabled=True
    )
    email = forms.EmailField(label="電子信箱", required=True)
    # phone = PhoneNumberField(label="連絡電話", region="TW", required=False) # 暫時先不用PhoneNumberField
    phone = forms.CharField(label="連絡電話", max_length=20, required=True)

    class Meta:
        model = Participant
        fields = [
            "username",
            "last_name",
            "first_name",
            "email",
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
            HTML(
                """
                <li class="help-text"><span>密碼不能和使用者名稱過度相似</span></li>
                <li class="help-text"><span>密碼長度至少要 8 個字元</span></li>
                <li class="help-text"><span>不能使用極為常見的密碼</span></li>
                <li class="help-text"><span>密碼不能只包含數字</span></li>
            """
            ),
            Field("password2", placeholder="請再次輸入密碼", css_class="center-field"),
            Field("last_name", placeholder="請輸入姓氏", css_class="center-field"),
            Field("first_name", placeholder="請輸入名稱", css_class="center-field"),
            Field("identity", css_class="center-field"),
            Field("phone", placeholder="請輸入連絡電話", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "註冊", css_class="btn-secondary"))


# 登入的表單
class LoginForm(AuthenticationForm):
    # 登入時的username是電子信箱
    username = UsernameField(
        label="電子信箱",
        max_length=150,
        required=True,
        error_messages={"required": "電子信箱或密碼錯誤"},
    )
    password = forms.CharField(
        label="密碼",
        max_length=200,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )

    error_messages = {
        "invalid_login": "電子信箱或密碼錯誤",
        "inactive": "This account is inactive.",
    }

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
                placeholder="請輸入電子信箱",
                css_class="center-field",
            ),
            Field("password", placeholder="請輸入密碼", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "登入", css_class="btn-secondary"))

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


# 建立業界專家個人資料
class ExpertInfoCreateForm(forms.ModelForm):
    company = forms.CharField(label="任職公司", max_length=50, required=True)
    title = forms.CharField(label="職稱", max_length=20, required=True)
    telephone = forms.CharField(label="辦公室電話", max_length=20, required=True)
    address = forms.CharField(label="聯絡地址", max_length=100, required=True)
    bank_account = forms.CharField(label="銀行(郵局)帳號", max_length=14, required=False)

    class Meta:
        model = ExpertInfo
        fields = [
            "company",
            "title",
            "address",
            "telephone",
            "bank_account",
        ]

    def __init__(self, *args, **kwargs):
        super(ExpertInfoCreateForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "expert-register-form"
        self.helper.layout = Layout(
            Field("company", placeholder="請輸入任職公司", css_class="center-field"),
            Field("title", placeholder="請輸入職稱", css_class="center-field"),
            Field("address", placeholder="請輸入聯絡地址", css_class="center-field"),
            Field("telephone", placeholder="請輸入辦公室電話", css_class="center-field"),
            Field("bank_account", placeholder="請輸入銀行(郵局)帳號", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))


# 建立學生代表個人資料
class StudentInfoCreateForm(forms.ModelForm):
    student_id = forms.CharField(label="學號", max_length=15, required=True)
    school_system = forms.CharField(
        label="學制",
        max_length=10,
        required=True,
    )
    grade = forms.CharField(label="年級", max_length=10, required=True)

    class Meta:
        model = StudentInfo
        fields = [
            "student_id",
            "school_system",
            "grade",
        ]

    def __init__(self, *args, **kwargs):
        super(StudentInfoCreateForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.layout = Layout(
            Field("student_id", placeholder="請輸入學號", css_class="center-field"),
            Field("school_system", placeholder="請輸入學制", css_class="center-field"),
            HTML(
                '<li class="help-text"><span class="help-text">例如：大學部、研究所</span></li>'
            ),
            Field("grade", placeholder="請輸入年級", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))


# 建立校外老師個人資料
class TeacherInfoCreateForm(forms.ModelForm):
    school = forms.CharField(label="任職學校", max_length=50, required=True)
    department = forms.CharField(label="系所", max_length=20, required=True)
    title = forms.CharField(label="職稱", max_length=20, required=True)
    telephone = forms.CharField(label="辦公室電話", max_length=20, required=True)
    address = forms.CharField(label="聯絡地址", max_length=100, required=True)
    bank_account = forms.CharField(label="銀行(郵局)帳號", max_length=14, required=False)

    class Meta:
        model = TeacherInfo
        fields = [
            "school",
            "department",
            "title",
            "telephone",
            "address",
            "bank_account",
        ]

    def __init__(self, *args, **kwargs):
        super(TeacherInfoCreateForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "teacher-register-form"
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
class AssistantInfoCreateForm(forms.ModelForm):
    telephone = forms.CharField(label="辦公室電話", max_length=20, required=True)

    class Meta:
        model = AssistantInfo
        fields = [
            "telephone",
        ]

    def __init__(self, *args, **kwargs):
        super(AssistantInfoCreateForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "assistant-register-form"
        self.helper.layout = Layout(
            Field("telephone", placeholder="請輸入辦公室電話", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))


# 建立系上老師個人資料
class ProfessorInfoCreateForm(forms.ModelForm):
    title = forms.CharField(label="職級", max_length=20, required=True)
    telephone = forms.CharField(label="辦公室電話", max_length=20, required=True)

    class Meta:
        model = ProfessorInfo
        fields = [
            "title",
            "telephone",
        ]

    def __init__(self, *args, **kwargs):
        super(ProfessorInfoCreateForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "professor-register-form"
        self.helper.layout = Layout(
            Field("title", placeholder="請輸入職級", css_class="center-field"),
            Field("telephone", placeholder="請輸入辦公室電話", css_class="center-field"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))


def get_info_create_form(method, user):
    if user.identity == 0:
        return ExpertInfoCreateForm(method, instance=user.expert_info)
    elif user.identity == 1:
        return StudentInfoCreateForm(method, instance=user.student_info)
    elif user.identity == 2:
        return TeacherInfoCreateForm(method, instance=user.teacher_info)
    elif user.identity == 3:
        return AssistantInfoCreateForm(method, instance=user.assistant_info)
    else:
        return ProfessorInfoCreateForm(method, instance=user.professor_info)


# admin後台顯示的表單
class ParticipantChangeForm(UserChangeForm):
    username = forms.CharField(label="使用者名稱", max_length=150, required=False)
    first_name = forms.CharField(label="名稱", max_length=10, required=False)
    last_name = forms.CharField(label="姓氏", max_length=10, required=False)
    password1 = forms.CharField(
        label="密碼",
        max_length=200,
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
        help_text="""<ul style="list-style-type:none; text-align:left">
                <li><span class="help-text">- 密碼不能和使用者名稱過度相似</span></li>
                <li><span class="help-text">- 密碼長度至少要 8 個字元</span></li>
                <li><span class="help-text">- 不能使用極為常見的密碼</span></li>
                <li><span class="help-text">- 密碼不能只包含數字</span><li>
            </ul>""",
    )
    password2 = forms.CharField(
        label="確認密碼",
        max_length=200,
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )
    identity = forms.ChoiceField(label="身分", choices=IDENTITY, required=False)
    email = forms.EmailField(label="電子信箱", required=False)
    # phone = PhoneNumberField(label="連絡電話", region="TW", required=False) # 暫時先不用PhoneNumberField
    phone = forms.CharField(label="連絡電話", max_length=20, required=False)

    class Meta:
        model = Participant
        fields = [
            "username",
            "last_name",
            "first_name",
            "email",
            "identity",
            "phone",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super(ParticipantChangeForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = "user-change-form"
        self.helper.layout = Layout(
            Field("username"),
            Field("email"),
            Field("password1"),
            Field("password2"),
            Field("last_name"),
            Field("first_name"),
            Field("identity"),
            Field("phone"),
        )
        self.helper.add_input(Submit("submit", "保存", css_class="btn-secondary"))
