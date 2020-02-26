from django.contrib import admin

# Register your models here.
from uxhub.models import User, Comment, ChangingMilestone, ChangingIssue, ChangingComment

admin.site.register(Comment)
admin.site.register(User)
admin.site.register(ChangingMilestone)
admin.site.register(ChangingIssue)
admin.site.register(ChangingComment)
