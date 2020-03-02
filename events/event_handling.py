def create_comment_event(pk):
    from uxhub.models import Comment, ChangingComment

    comment = Comment.objects.get(pk=pk)
    comment_event = ChangingComment(description=comment.description, issues=comment.issues,
                                    users=comment.users, comment=comment)
    comment_event.save()


def create_milestone_event(pk):
    from uxhub.models import Milestone, ChangingMilestone

    milestone = Milestone.objects.get(pk=pk)
    milestone_event = ChangingMilestone(milestones=milestone, name=milestone.name, projects=milestone.projects,
                                        start_date=milestone.start_date, end_date=milestone.end_date)
    milestone_event.save()


def create_issue_event(pk):
    from uxhub.models import Issue, ChangingIssue, User

    issue = Issue.objects.get(pk=pk)
    issue_event = ChangingIssue(issues=issue, new_state=issue.state)
    issue_event.save()
    issue_event.assignees.set(issue.users.all())
