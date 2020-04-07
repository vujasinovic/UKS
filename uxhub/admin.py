from django.contrib import admin

# Register your models here.
from uxhub.models import Project, Milestone, Issue, GithubUser

admin.site.register(Project)
admin.site.register(Milestone)
admin.site.register(Issue)
admin.site.register(GithubUser)
