from django.http import HttpResponse

from .students import get_students, get_linked_students
from logo import get_logo

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

    get_logo()

    s.append('<link rel="shortcut icon" type="image/png" href="favicon.png"/>')
    s.append('<img href="images/org_logo.png">')
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
    return HttpResponse('\n'.join(s))
