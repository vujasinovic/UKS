from django.db import models

# Create your models here.


class Project(models.Model):
    project_name = models.CharField()
    git_repository_url = models.URLField()


class Milestone(models.Model):
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()


class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    milestones = models.ForeignKey(Milestone)
    start_date = models.DateField()
    end_date = models.DateField()
    approximated_time = models.TimeField()
    invested_time = models.TimeField()
    completion = models.IntegerField()
    issue_name = models.CharField()
    description = models.CharField()


class Label(models.Model):
    issues = models.ManyToManyField(Issue)
    label_name = models.CharField()
    label_color = models.CharField()


class User(models.Model):
    issues = models.ManyToManyField(Issue)
    name = models.CharField()
    email = models.EmailField()
    projects = models.ForeignKey(Project)


class GithubUser(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField()


class Commit(models.Model):
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)
    url = models.URLField
    comment = models.CharField()
    invested_time = models.TimeField()


class Event(models.Model):
    issues = models.ForeignKey(Issue, on_delete=models.CASCADE)
    time = models.TimeField()
    users = models.ForeignKey(User)

    class Meta:
        abstract = True


class ChangingComment(Event):
    comment = models.CharField()


class ChangingState(Event):
    new_state = models.enums


class ChangingAssignee(Event):
    assignee = User()


class Comment(Event):
    description = models.CharField()


class ChangingMilestone(Event):
    milestones = models.ForeignKey(Milestone)

