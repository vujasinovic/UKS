from django.shortcuts import render
from django.views.generic import ListView

from uxhub.models import Commit, Project


class CommitList(ListView):
    model = Commit


def commit_list(request):
    project_name = get_param(request, 'project')
    branch_name = get_param(request, 'branch')

    if project_name:
        project = Project.objects.get(name=project_name)
        branch_names = Commit.objects.filter(projects=project).values_list('branch', flat=True)
        if branch_name:
            commits = Commit.objects.filter(projects=project, branch=branch_name)
        else:
            commits = Commit.objects.filter(projects=project)
    else:
        if branch_name:
            commits = Commit.objects.filter(branch=branch_name)
        else:
            commits = Commit.objects.filter()
        branch_names = Commit.objects.all().values_list('branch', flat=True)

    project_names = Project.objects.all().values_list('name', flat=True)

    return render(request, 'uxhub/commit_list.html',
                  {"commits": commits,
                   "project_names": project_names, "selected_project": project_name,
                   "branch_names": set(branch_names), "selected_branch": branch_name})


def get_param(request, name):
    try:
        return request.GET[name]
    except:
        return None
