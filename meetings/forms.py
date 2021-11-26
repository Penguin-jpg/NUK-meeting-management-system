# from django import forms
# from .models import Meeting


# class MeetingCreateForm(forms.ModelForm):
#     name = forms.CharField(max_length=100, unique=True)  # 名稱
#     type = forms.CharField(max_length=20, null=False)  # 種類
#     date = forms.DateField(null=False)  # 日期
#     location = forms.CharField(max_length=100, null=False)  # 地點
#     chairman = forms.CharField(max_length=20, null=False)  # 主席
#     minutes_taker = forms.CharField(max_length=20, null=False)  # 記錄人員

#     class Meta:
#         model = Meeting
#         fields = [
#             "name",
#             "type",
#             "date",
#             "location",
#             "chairman",
#             "minutes_taker",
#         ]
