from calendar import HTMLCalendar
from .models import Meeting


# 日歷
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # 將day格式化成td
    # 由day來找出會議
    def formatday(self, day, meetings):
        meetings = meetings.filter(date__day=day)
        date = ""

        # 只需要一個超連結就好
        for meeting in meetings:
            date += f'<span class="meeting-link">{meeting.get_url}</span>'
            break

        if day != 0:
            return f'<td><div class="day">{day}</div>{date}</td>'
        return "<td></td>"

    # 將week格式化成tr
    def formatweek(self, theweek, meetings):
        week = ""
        for day, _ in theweek:
            week += self.formatday(day, meetings)
        return f"<tr>{week}</tr>"

    # 將month格式化成table
    # 由month,year來找出會議
    def formatmonth(self, withyear=True):
        meetings = Meeting.objects.filter(date__year=self.year, date__month=self.month)

        print(self.year, self.month)

        for meeting in meetings:
            print(meeting.date)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f"{self.formatmonthname(self.year, self.month, withyear=withyear)}\n"
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, meetings)}\n"
        return cal
