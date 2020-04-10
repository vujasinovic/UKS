from datetime import datetime
from time import strptime, mktime

from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import make_aware
from github.Event import Event as GithubEvent
from pydispatch import dispatcher

from uxhub.models import Project, Commit, User, Issue, ChangingIssue, GithubUser, Milestone


def catch_event(event_name):
    """
    Register event handler.
    All names can be found at https://developer.github.com/v3/activity/events/types/
    """

    def inner(func):
        dispatcher.connect(func, signal=event_name, sender=dispatcher.Any)
        return func

    return inner


def send_github_event(event: GithubEvent):
    try:
        dispatcher.send(signal=event.type, event=event, sender=dispatcher.Anonymous)
    except Exception as ex:
        print(ex)


@catch_event("PushEvent")
def handle_push(event):
    project_name = event.repo.full_name
    project = Project.objects.get(name=project_name)

    branch = event.payload['ref'].replace("refs/heads/", "")
    date = make_aware(event.created_at)

    for commit in event.payload['commits']:
        author_username = event.actor.login
        author = get_user(author_username)

        commit_entity = Commit(
            projects=project,
            author=author,
            comment=commit['message'],
            sha=commit['sha'],
            branch=branch,
            date=date)
        commit_entity.save()

        link_issue(commit_entity)


def link_issue(commit: Commit):
    try:
        identifier = commit.comment.split(" - ")[0].strip()
        issue = Issue.objects.get(name__startswith=identifier, project=commit.projects)

        if issue:
            commit.issues = issue
            commit.save()
    except:
        pass


def get_user(username):
    try:
        user = GithubUser.objects.get(username=username).users
    except ObjectDoesNotExist:
        user = User(username=username)
        user.save()
        GithubUser(username=username, users=user).save()

    return user


@catch_event("IssuesEvent")
def handle_issue_event(event):
    issue = get_issue(event)
    payload = event.payload
    date = make_aware(event.created_at)
    github_issue = payload['issue']
    action = payload['action']

    if action.endswith("opened"):
        issue.state = "OPENED"
    elif action == "closed":
        issue.state = "CLOSED"
    elif action == "edited":
        issue.name = github_issue['title']
        issue.description = github_issue['body']
    issue.save(skip_log=True)

    changing_issue = ChangingIssue(
        new_state=issue.state,
        issues=issue,
        time=date,
        author=get_user(event.actor.login))
    changing_issue.save()

    assignee_info = payload['issue']['assignee']
    if assignee_info:
        assignee = get_user(assignee_info['login'])

        issue.assignee.add(assignee)
        changing_issue.assignees.add(assignee)

        issue.save()
        changing_issue.save()

    milestone = event.payload['issue']['milestone']
    if milestone:
        milestone_id = int(event.payload['issue']['milestone']['id'])

        try:
            milestone_entity = Milestone.objects.get(id=milestone_id)
        except:
            milestone_entity = Milestone(id=milestone_id)

        datetime_format = "%Y-%m-%dT%H:%M:%S%z"
        milestone_entity.start_date = datetime.fromtimestamp(mktime(strptime(milestone['created_at'], datetime_format)))
        milestone_entity.end_date = datetime.fromtimestamp(mktime(strptime(milestone['due_on'], datetime_format)))
        milestone_entity.name = milestone['title']
        milestone_entity.projects = issue.project
        milestone_entity.save()

        issue.milestones = milestone_entity
        issue.save()


def get_issue(event):
    issue_id = event.payload['issue']['id']
    issue = None

    try:
        issue = Issue.objects.get(github_id=issue_id)
    except ObjectDoesNotExist:
        issue = create_issue(event)

    return issue


def create_issue(event):
    payload = event.payload
    github_issue = payload['issue']

    issue = Issue(
        name=github_issue['title'],
        description=github_issue['body'],
        project=Project.objects.get(name=event.repo.name),
        github_id=github_issue['id'],
        github_url=github_issue['html_url'],
        state='TO_DO',
        completion=False
    )
    issue.save(skip_log=True)

    return issue


@catch_event("MilestoneEvent")
def handle_milestone_event(event):
    pass
