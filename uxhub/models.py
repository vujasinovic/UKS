from django.contrib.auth.models import User as AuthUser
from django.db import models
# Create your models here.
from django.utils.timezone import now


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username


class Project(models.Model):
    name = models.CharField(max_length=200)
    git_repository_url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    collaborators = models.ManyToManyField(User, related_name='collaborators')

    def __str__(self):
        return self.name


class GithubProjectSync(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_time_started = models.DateTimeField()


class GithubEvent(models.Model):
    project_sync = models.ForeignKey(GithubProjectSync, on_delete=models.CASCADE)
    github_id = models.IntegerField()
    type = models.CharField(max_length=256)


class Milestone(models.Model):
    name = models.CharField(max_length=200, default='')
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField()

    def __str__(self):
        return self.name


ISSUE_STATUS = (
    ('OPEN', 'Open'),
    ('CLOSED', 'Closed'),
)


class Issue(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    milestones = models.ForeignKey(Milestone, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    approximated_time = models.IntegerField(null=True)
    invested_time = models.IntegerField(null=True)
    completion = models.BooleanField()
    assignee = models.ManyToManyField(User, blank=True)
    state = models.CharField(max_length=8, choices=ISSUE_STATUS, default='OPEN')
    github_id = models.IntegerField(null=True)
    github_url = models.CharField(max_length=512, null=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    issues = models.ManyToManyField(Issue)
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=20)


class GithubUser(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=30)
    access_token = models.CharField(max_length=256, null=True)


class Commit(models.Model):
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)
    issues = models.ForeignKey(Issue, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField
    comment = models.CharField(max_length=200)
    invested_time = models.TimeField(null=True)
    github_id = models.IntegerField(null=True)
    branch = models.CharField(max_length=255, null=True)
    sha = models.CharField(max_length=256, null=True)
    date = models.DateTimeField(null=True)


class Event(models.Model):
    issues = models.ForeignKey(Issue, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(default=now, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class ChangingIssue(Event):
    new_state = models.CharField(max_length=8, choices=ISSUE_STATUS, default='TO_DO')
    assignees = models.ManyToManyField(User, related_name='issue_assignees')
    github_url = models.CharField(max_length=512, null=True)


class Comment(Event):
    description = models.CharField(max_length=400)


class ChangingComment(Event):
    description = models.CharField(max_length=400)
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)


class ChangingMilestone(Event):
    milestones = models.ForeignKey(Milestone, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, default='')
    projects = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)
