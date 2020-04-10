import sys
import threading
from datetime import datetime
from time import sleep

from django.utils.timezone import make_aware

from github_sync.github_api import get_events
from github_sync.github_event_handler import send_github_event
from uxhub.models import Project, GithubEvent, GithubProjectSync

sync_interval = 5 * 60


def setup_sync_scheduler():
    x = threading.Thread(target=sync_all_projects_loop)
    x.start()


def sync_all_projects_loop():
    while True:
        sync_all_projects()
        sleep(sync_interval)


def sync_all_projects():
    projects = Project.objects.all()
    for project in projects:
        sync_project(project, False)


def sync_project_async(project: Project, new_project=False):
    x = threading.Thread(target=sync_project, args=(project, new_project))
    x.start()


def sync_project(project: Project, new_project):
    print("Syncing Github project " + project.name)
    events = get_events(project)

    if events:
        project_sync = GithubProjectSync(project=project, date_time_started=make_aware(datetime.now()))
        project_sync.save()

        for e in events:
            print("Processing " + e.type + ", id=" + e.id)
            try:
                send_github_event(e)
                GithubEvent(project_sync=project_sync, github_id=e.id, type=e.type).save()
            except Exception as exception:
                print("Failed to process GithubEvent " + e.type + ", id=" + e.id, file=sys.stderr)
                print(exception)
            project_sync.save()

    print("Sync completed")
