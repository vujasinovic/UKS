from django.db import models
from django.contrib.auth.models import User as AuthUser
# Create your models here.
from django.utils.timezone import now

from events.event_handling import create_comment_event, create_milestone_event, create_issue_event


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Project(models.Model):
    name = models.CharField(max_length=200)
    git_repository_url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    collaborators = models.ManyToManyField(User, related_name='collaborators')

    def __str__(self):
        return self.project_name


class Milestone(models.Model):
    name = models.CharField(max_length=200, default='')
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        create_milestone_event(self.pk)


ISSUE_STATUS = (
        ('TO_DO', 'To do'),
        ('OPENED', 'Opened'),
        ('FEEDBACK', 'Requested feedback'),
        ('CLOSED', 'Closed')
)


class Issue(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    milestones = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    approximated_time = models.IntegerField()
    invested_time = models.IntegerField()
    completion = models.BooleanField()
    assignee = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        create_issue_event(self.pk)


class Label(models.Model):
    issues = models.ManyToManyField(Issue)
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=20)


class GithubUser(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=30)


class Commit(models.Model):
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)
    issues = models.ForeignKey(Issue, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField
    comment = models.CharField(max_length=200)
    invested_time = models.TimeField()


class Event(models.Model):
    issues = models.ForeignKey(Issue, on_delete=models.CASCADE)
    time = models.TimeField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class ChangingIssue(Event):
    new_state = models.CharField(max_length=8, choices=ISSUE_STATUS, default='TO_DO')
    assignees = models.ManyToManyField(User, related_name='issue_assignees')


class Comment(Event):
    description = models.CharField(max_length=400)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        create_comment_event(self.pk)


class ChangingComment(Event):
    description = models.CharField(max_length=400)
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)


class ChangingMilestone(Event):
    milestones = models.ForeignKey(Milestone, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, default='')
    projects = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)

