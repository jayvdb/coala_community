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
        s.append('<li><a href="{student_url}">{student_id}</a>:<br />'
                 '<div class="github-card" data-github="{username}" '
                 'data-width="400" data-height="" data-theme="default"></div>'
                 .format(student_url=student_url, student_id=student_id,
                         username=username))

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    s.append('</ul><i id="time" class="timestamp" data-time="{unix}">'
             'Last updated: {timestamp} '
             '(<span id="ago" class="timeago"></span>)</i>'
             .format(unix=timegm(datetime.utcnow().utctimetuple()),
                     timestamp=timestamp))

    s.append('<script src="//cdn.jsdelivr.net/github-cards/latest/widget.js">'
             '</script>')
    s.append('<script src="static/timeago.js"></script>')
    s.append('<script>loadTimeElements()</script>')

    return HttpResponse('\n'.join(s))
