from django.db import models
from django.contrib.auth.models import User as AuthUser
# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)

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


class ChangingComment(Event):
    comment = models.CharField(max_length=400)


class ChangingState(Event):
    new_state = models.enums


class ChangingAssignee(Event):
    assignee = User()


class Comment(Event):
    description = models.CharField(max_length=400)


class ChangingMilestone(Event):
    milestones = models.ForeignKey(Milestone, on_delete=models.SET_NULL, null=True)

