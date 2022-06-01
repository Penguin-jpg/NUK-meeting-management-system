from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import threading
import os

# 因為寄信要花很久，所以用多執行緒讓main thread輕鬆一點
class EmailThread(threading.Thread):
    def __init__(self, meeting, subject, template, context):
        self.meeting = meeting
        self.subject = subject
        self.template = template
        self.context = context
        threading.Thread.__init__(self)

    def run(self):
        formatted_date = self.meeting.date.strftime("%Y/%m/%d %H:%M")  # 格式化日期
        html_body = render_to_string(
            os.path.join(settings.TEMPLATES[0]["DIRS"][0], self.template),
            context=self.context,
        )
        message = EmailMultiAlternatives(
            subject="高雄大學資訊工程學系會議管理系統 - 會議通知",  # 標題
            body=f"您好，您參加的會議「{self.meeting.name}」（{self.meeting.get_type_display()}）將在 {formatted_date} 於{self.meeting.location}舉行，以下為會議議程：\n\n",  # 內容
            from_email=settings.EMAIL_HOST_USER,  # 寄信人
            to=[
                participant.email for participant in self.meeting.participants.all()
            ],  # 　收信人
        )
        message.attach_alternative(html_body, "text/html")
        message.send(fail_silently=False)
