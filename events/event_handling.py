from uxhub.models import Comment, ChangingComment, User, Milestone, ChangingMilestone, Issue, ChangingIssue


def create_comment_event(pk):
    comment = Comment.objects.get(pk=pk)
    comment_event = ChangingComment(description=comment.description, issues=comment.issues,
                                    author=comment.author, comment=comment)
    comment_event.save()


def create_milestone_event(pk, auth_user):
    logged_author = User.objects.get(auth_user=auth_user)

    milestone = Milestone.objects.get(pk=pk)
    milestone_event = ChangingMilestone(
        milestones=milestone,
        name=milestone.name,
        projects=milestone.projects,
        start_date=milestone.start_date,
        end_date=milestone.end_date,
        author=logged_author
    )
    milestone_event.save()


def create_issue_event(pk, auth_user):
    logged_author = User.objects.get(auth_user=auth_user)

    issue = Issue.objects.get(pk=pk)
    issue_event = ChangingIssue(issues=issue, new_state=issue.state, author=logged_author)
    issue_event.save()
    issue_event.assignees.set(issue.assignee.all())
