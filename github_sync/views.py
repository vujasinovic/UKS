import requests
from django.contrib.auth.models import User as AuthUser

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render
from github import Github

from github_sync.github_api import create_github_client
from github_sync.github_sync import sync_project_async
from uxhub.models import GithubUser, User, Project

# Create your views here.

client_id = '4d1d53b66942c6f016a0'
client_secret = '5486b56fd66259b031a90c89fd02f99eb1496393'


def github_authorize(request):
    code = request.GET['code']

    url = 'https://github.com/login/oauth/access_token'

    response = requests.post(url, data={
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'scope': 'repo'
    })

    raw = response.text
    access_token = raw.split('access_token=')[1].split('&')[0]

    try:
        user = User.objects.get(username=request.user.username)
    except:
        auth_user = request.user
        user = User(username=auth_user.username, auth_user=auth_user)
        user.save()

    try:
        github_user = GithubUser.objects.get(users=user)
        github_user.access_token = access_token
        github_user.save()
    except:
        github_api = Github(access_token)
        github_user = github_api.get_user()
        GithubUser(users=user, access_token=access_token, username=github_user.login).save()

    return redirect('/github/projects')


def github_project_list(request):
    projects = None

    try:
        projects = get_github_client(request).get_user().get_repos().reversed

        for project in projects:
            try:
                project.uxhub_id = Project.objects.get(name=project.full_name).id
            except:
                pass
    except:
        pass

    return render(request, 'uxhub/github_projects.html', {"client_id": client_id, "projects": projects})


def github_project_import(request):
    name = request.POST['name']
    repo = get_github_client(request).get_repo(name)

    project = Project(
        name=repo.full_name,
        git_repository_url=repo.html_url,
        owner=User.objects.get(auth_user=request.user))
    project.save()

    sync_project_async(project, new_project=True)

    return redirect('/projects/view/' + str(project.id))


def get_github_client(request):
    auth_user = User.objects.get(username=request.user.username)
    github_user = GithubUser.objects.get(users=auth_user)
    return create_github_client(github_user)


def get_user(username):
    user = None
    try:
        user = GithubUser.objects.get(username=username).users
    except ObjectDoesNotExist:
        user = User(username=user)
        user.save()
        GithubUser(username=username, users=user).save()

    return user
