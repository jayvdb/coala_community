from django.http import HttpResponse
from datetime import datetime
from calendar import timegm

from .students import get_students, get_linked_students

STUDENT_URL = (
    'https://codein.withgoogle.com/dashboard/task-instances/?'
    'sp-organization={org_id}&sp-claimed_by={student_id}'
    '&sp-order=-modified&sp-my_tasks=false&sp-page_size=20'
)


def index(request):
    linked_students = list(get_linked_students(get_students()))
    org_id = linked_students[0]['organization_id']
    org_name = linked_students[0]['organization_name']
    s = []
    s.append('<h2>Welcome</h2>')
    s.append('Hello, world. You are at the {org_name} community GCI website.'
             .format(org_name=org_name))
    s.append('Students linked to %s issues:<ul>' % org_name)
    for student in linked_students:
        student_id = student['id']
        username = student['username']
        student_url = STUDENT_URL.format(org_id=org_id,
                                         student_id=student_id,
                                         )
        s.append('<li><a href="{student_url}">{student_id}</a>: '
                 '<a href="https://github.com/{username}">{username}</a>'
                 .format(student_url=student_url, student_id=student_id,
                         username=username))
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    s.append('</ul><i id="time" data-time="{unix}">'
             'Last updated: {timestamp} (<span id="ago"></span>)</i>'
             .format(unix=timegm(datetime.utcnow().utctimetuple()),
                     timestamp=timestamp))
    s.append('<script>'
             'var time = document.getElementById("time");'
             'var ago = document.getElementById("ago");'
             'var timestamp = time.getAttribute("data-time");'
             'var sec = ((new Date()).getTime() / 1000) - parseInt(timestamp);'
             'var min = sec / 60;'
             'var hour = min / 60;'
             'var day = hour / 24;'
             'var timeString = "";'
             'if (day > 1) {'
             '  timeString = `${parseInt(day)} days ago`;'
             '} else {'
             '  timeString = `${parseFloat(hour).toFixed(2)} hours ago`;'
             '}'
             'ago.innerHTML = timeString;'
             '</script>')

    return HttpResponse('\n'.join(s))
