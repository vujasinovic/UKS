from uxhub.models import Project, User, Milestone, Issue, Comment
from django.contrib.auth.models import User as AuthUser
import datetime


def create_auth_user():
    return AuthUser.objects.create_user(
        username='lukajvnv',
        password='Luka2903',
        email='lukajvnv@gmail.com'
    )


def create_user(auth_obj_user):
    return User.objects.create(
        username='lukajvnv',
        email='lukajvnv@gmail.com',
        auth_user=auth_obj_user
    )


def create_project(proj_owner):
    return Project.objects.create(
        name='Uxhub',
        git_repository_url='http://127.0.0.1:8000/events/milestones_log/6',
        owner=proj_owner
    )


def create_milestone(proj):
    today = datetime.date.today()
    return Milestone.objects.create(
        name='Milestone 1',
        projects=proj,
        start_date=today,
        end_date=today + datetime.timedelta(days=10)
    )


def create_issue(proj, mile, cur_state='OPEN'):
    today = datetime.date.today()
    return Issue.objects.create(
        name='Issue 1',
        description="Desc",
        project=proj,
        milestones=mile,
        start_date=today,
        end_date=today + datetime.timedelta(days=10),
        approximated_time=5,
        invested_time=2,
        completion=False,
        state=cur_state
    )


def create_comment(iss, user, text):
    return Comment.objects.create(
        issues=iss,
        author=user,
        description=text
    )