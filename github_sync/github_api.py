from github import Github

from uxhub.models import GithubUser, Project, GithubEvent


def create_github_client(github_user: GithubUser):
    return Github(github_user.access_token)


def get_events(project: Project):
    repository = get_api_repository(project)
    processed_events = GithubEvent.objects.all().values_list('github_id', flat=True)

    events = repository.get_events()
    response = []

    for event in events:
        if int(event.id) in processed_events:
            break
        response.insert(0, event)

    return response


def get_issues(project: Project):
    repository = get_api_repository(project)
    issues = repository.get_issues()
    return issues


def get_commits(project: Project):
    repository = get_api_repository(project)
    commits = repository.get_commits()
    return commits


def get_milestones(project: Project):
    repository = get_api_repository(project)
    milestones = repository.get_milestones()
    return milestones


def get_api_repository(project: Project):
    github = create_github_client(get_any_github_user(project))
    repository = github.get_repo(project.name)
    return repository


def get_any_github_user(repository: Project):
    """
    Return any known user that has access to repository.
    """

    user = repository.owner
    return GithubUser.objects.get(users=user)
