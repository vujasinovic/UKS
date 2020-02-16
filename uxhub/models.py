from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    git_repository_url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Milestone(models.Model):
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()


class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    milestones = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    approximated_time = models.TimeField()
    invested_time = models.TimeField()
    completion = models.IntegerField()
    issue_name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    users = models.ManyToManyField(User)


class Label(models.Model):
    issues = models.ManyToManyField(Issue)
    label_name = models.CharField(max_length=20)
    label_color = models.CharField(max_length=20)


class GithubUser(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=30)


class Commit(models.Model):
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)
    url = models.URLField
    comment = models.CharField(max_length=200)
    invested_time = models.TimeField()


class Event(models.Model):
    issues = models.ForeignKey(Issue, on_delete=models.CASCADE)
    time = models.TimeField()
    users = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

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

