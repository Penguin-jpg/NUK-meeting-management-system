from django import forms
from django.contrib.auth.forms import (
    PasswordChangeForm,
    UserCreationForm,
    UserChangeForm,
    UsernameField,
    AuthenticationForm,
)
from .models import Participant, Profile
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Div, Row, Column, Field, HTML

SEX = ((0, "女性"), (1, "男性"))
IDENTITY = (
    (0, "業界專家"),
    (1, "學生代表"),
    (2, "校外老師"),
    (3, "系助理"),
    (4, "系上老師"),
)


def password1_help_text():
    pass


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
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )
    type = forms.ChoiceField(label="身分", choices=IDENTITY, required=True)
    email = forms.EmailField(label="電子信箱", required=True)
    phone = PhoneNumberField(label="連絡電話", region="TW", required=False)

    class Meta:
        model = Participant
        fields = [
            "username",
            "last_name",
            "first_name",
            "email",
            "type",
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
            Field("username", placeholder="請輸入使用者名稱"),
            Field("email", placeholder="請輸入電子信箱"),
            Field("password1", placeholder="請輸入密碼"),
            Field("password2", placeholder="請再次輸入密碼"),
            Field("last_name", placeholder="請輸入姓氏"),
            Field("first_name", placeholder="請輸入名稱"),
            Field("type"),
            Field("phone", placeholder="請輸入連絡電話"),
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
            Field("username", placeholder="請輸入使用者名稱"),
            Field("password", placeholder="請輸入密碼"),
        )
        self.helper.add_input(Submit("submit", "登入", css_class="btn-secondary"))


# admin後台修改使用者的表單
class ParticipantChangeForm(UserChangeForm):
    username = forms.CharField(label="使用者名稱", max_length=150, required=False)
    first_name = forms.CharField(label="名稱", max_length=10, required=False)
    last_name = forms.CharField(label="姓氏", max_length=10, required=False)
    type = forms.ChoiceField(label="身分", choices=IDENTITY, required=False)
    email = forms.EmailField(label="電子信箱", required=False)
    phone = PhoneNumberField(label="連絡電話", region="TW", required=False)

    class Meta:
        model = Participant
        fields = [
            "username",
            "last_name",
            "first_name",
            "password",
            "email",
            "type",
            "phone",
        ]

    def __init__(self, *args, **kwargs):
        super(ParticipantChangeForm, self).__init__(*args, **kwargs)
        self.fields["password"].label = "密碼"


# 個人資料的編輯表格
class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(label="電子信箱", required=False)
    sex = forms.ChoiceField(label="性別", choices=SEX, initial=0, required=False)
    phone = PhoneNumberField(label="連絡電話", region="TW", required=False)
    telephone = PhoneNumberField(label="辦公室電話", region="TW", required=False)
    company = forms.CharField(label="任職公司", max_length=50, required=False)
    address = forms.CharField(label="聯絡地址", max_length=100, required=False)
    title = forms.CharField(label="職稱", max_length=20, required=False)
    bank_account = forms.CharField(label="銀行(郵局)帳號", max_length=14, required=False)
    student_id = forms.CharField(label="學號", max_length=15, required=False)
    school_system = forms.CharField(
        label="學制",
        max_length=10,
        help_text="""<ul style="list-style-type:none; text-align:left"><li><span class="help-text">例如：大學部、研究所</span></li></ul>""",
        required=False,
    )
    grade = forms.CharField(label="年級", max_length=10, required=False)
    school = forms.CharField(label="任職學校", max_length=50, required=False)
    department = forms.CharField(label="系所", max_length=20, required=False)

    class Meta:
        model = Profile
        fields = [
            "sex",
            "email",
            "phone",
            "telephone",
            "company",
            "address",
            "title",
            "bank_account",
            "school",
            "student_id",
            "department",
            "school_system",
            "grade",
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        # 取得目前的profile
        instance = kwargs["instance"]
        print(instance)
        data = {
            "user": instance.user,
            "sex": instance.sex,
            "email": instance.email,
            "phone": instance.phone,
            "telephone": instance.telephone,
            "title": instance.title,
            "address": instance.address,
            "bank_account": instance.bank_account,
            "company": instance.company,
            "school": instance.school,
            "department": instance.department,
            "student_id": instance.student_id,
            "school_system": instance.school_system,
            "grade": instance.grade,
        }
        self.initial = data  # 初始值

        # crispy form
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "blueForms"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-12 col-md-4 col-lg-2"
        self.helper.field_class = "col-sm-12 col-md-6 col-lg-8"
        self.helper.form_id = "edit-profile-form"
        # 共通欄位
        self.helper.layout = Layout(
            Field("email"),
            Field("sex"),
            Field("phone"),
        )

        # 根據type不同決定新增的欄位
        if instance.is_expert():
            self.helper.layout.extend(
                [
                    Field("telephone"),
                    Field("company"),
                    Field("address"),
                    Field("title"),
                    Field("banck_account"),
                ]
            )
        elif instance.is_student():
            self.helper.layout.extend(
                [Field("student_id"), Field("school_system"), Field("grade")]
            )
        elif instance.is_teacher():
            self.helper.layout.extend(
                [
                    Field("school"),
                    Field("address"),
                    Field("department"),
                    Field("title"),
                    Field("banck_account"),
                ]
            )
        elif instance.is_assistant():
            self.helper.layout.extend([Field("telephone")])
        elif instance.is_professor():
            self.helper.layout.extend([Field("telephone"), Field("title")])

        self.helper.add_input(Submit("submit", "修改", css_class="btn-secondary"))