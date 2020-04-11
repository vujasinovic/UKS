from django.test import TestCase

from events.event_handling import create_issue_event
from events.tests.test_utils import create_project, create_user, create_milestone, create_auth_user, create_issue, \
    create_comment
from uxhub.models import Comment, Issue, ChangingIssue


class TestModels(TestCase):
    def setUp(self):
        self.auth_user = create_auth_user()
        self.user = create_user(self.auth_user)
        self.project = create_project(self.user)
        self.milestone = create_milestone(self.project)
        self.issue = create_issue(self.project, self.milestone)

        self.issue_id = self.issue.id
        create_issue_event(self.issue_id, self.auth_user)

    def test_adding_new_comment(self):
        first_comment = create_comment(self.issue, self.user, 'First comment')

        comments_before_add = Comment.objects.all()
        comments_before_len = comments_before_add.count()

        new_comment = create_comment(self.issue, self.user, 'New comment')

        comments_after_add = Comment.objects.order_by('-time')
        last_added_com = comments_after_add[0]
        comments_after_len = comments_after_add.count()

        self.assertEqual(comments_before_len + 1, comments_after_len)
        self.assertEqual(new_comment.description, last_added_com.description)

    def test_issue_update(self):
        issue_before_update = Issue.objects.get(pk=self.issue_id)
        # SET TO OPEN BY DEFAULT
        issue_state_before_update = issue_before_update.state

        issue_before_update.state = 'CLOSED'
        issue_before_update.save()

        issue_after_update = Issue.objects.get(pk=self.issue_id)
        issue_state_after_update = issue_after_update.state

        # update occured
        self.assertNotEqual(issue_state_before_update, issue_state_after_update)

    def test_issue_update_changing_event_created(self):
        issue = Issue.objects.get(pk=self.issue_id)

        # SET TO OPEN BY DEFAULT
        issue_state_before_update = issue.state
        issue_events_before = ChangingIssue.objects.filter(issues__id=self.issue_id).order_by('-time')
        issue_events_before_latest = issue_events_before[0]
        issue_events_before_len = issue_events_before.count()

        # UPDATE
        issue_state_after_update = 'CLOSED'
        issue.state = issue_state_after_update
        issue.save()
        create_issue_event(self.issue_id, self.auth_user)

        issue_events_after = ChangingIssue.objects.filter(issues__pk=self.issue_id).order_by('-time')
        issue_events_after_len = issue_events_after.count()
        issue_events_after_latest = issue_events_after[0]

        # new event added
        self.assertEqual(issue_events_before_len + 1, issue_events_after_len)

        # old value
        self.assertEqual(issue_events_before_latest.new_state, issue_state_before_update)
        # new event value set correct
        self.assertEqual(issue_events_after_latest.new_state, issue_state_after_update)
