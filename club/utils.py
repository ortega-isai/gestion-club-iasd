from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Miembro


class Calendar(HTMLCalendar):
    # https://github.com/huiwenhw/django-calendar/tree/master
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter miembros by day
    def formatday(self, day, miembros):
        miembros_per_day = miembros.filter(fecha_nacimiento__day=day)
        d = ''
        for miembro in miembros_per_day:
            d += f''' <div class="event">
<div class="event-desc">
    {miembro}
</div>
<div class="event-time">
    Cumple {miembro.edad_por_anio} años
</div>
</div>'''
#             d += f'''<li>
# <span class="fw-bold"> {miembro}</span>
# <span class="badge text-bg-primary">{miembro.edad_por_anio}</span>
# </li>'''

        if day != 0:
            return f"<td><div class='date'>{day}</div>{d}</td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, miembros):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, miembros)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter miembros by month
    def formatmonth(self, withyear=True):
        miembros = Miembro.objects.filter(
            fecha_nacimiento__month=self.month
        )

        cal = f''
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, miembros)}\n'
        return cal
