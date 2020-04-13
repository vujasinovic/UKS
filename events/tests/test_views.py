from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse

from events.event_handling import create_comment_event, create_issue_event
from events.tests.test_utils import create_project, create_user, create_milestone, create_auth_user, create_issue, \
    create_comment


class TestView(TestCase):
    def setUp(self):
        self.client = Client()

        self.milestone_id = 1
        self.issue_id = 1
        self.non_existed_milestone_id = 5

        self.milestone_log_url = reverse('events:milestone_log', kwargs={'pk': self.milestone_id})
        self.issue_log_url = reverse('events:issue_log', kwargs={'pk': self.issue_id})
        self.all_comments_url = reverse('events:comment_list')
        self.comment_by_issue_url = reverse('events:comment_list_for_issue', kwargs={'issue_id': self.issue_id})
        self.new_comment_url = reverse('events:comment_new')

        self.username = 'lukajvnv'
        self.password = 'Luka2903'
        self.invalid_password = 'blabla'

        self.auth_user = create_auth_user()
        self.user = create_user(self.auth_user)
        self.project = create_project(self.user)
        self.milestone = create_milestone(self.project)
        self.issue = create_issue(self.project, self.milestone)
        create_issue_event(self.issue_id, self.auth_user)

        self.client.login(username=self.username, password=self.password)

    def test_milestone_log_GET(self):
        response = self.client.get(self.milestone_log_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'uxhub/milestone_log.html')

    def test_non_existed_milestone_log_GET(self):
        non_existed_milestone_log_url = reverse('events:milestone_log', kwargs={'pk': self.non_existed_milestone_id})
        response = self.client.get(non_existed_milestone_log_url)

        http_status_not_found = 404
        self.assertEqual(response.status_code, http_status_not_found)

    def test_comment_get_all_comments_GET(self):
        second_issue = create_issue(self.project, self.milestone)
        first_comment = create_comment(self.issue, self.user, '1st comment 1st issue')
        second_comment = create_comment(self.issue, self.user, '2nd comment 1st issue')
        third_comment = create_comment(second_issue, self.user, '1st comment 2nd issue')

        response = self.client.get(self.all_comments_url)
        all_comments = response.context_data['comment_list']

        self.assertEqual(all_comments.count(), 3)

    def test_comment_get_by_issue_GET(self):
        second_issue = create_issue(self.project, self.milestone)
        first_comment = create_comment(self.issue, self.user, '1st comment 1st issue')
        second_comment = create_comment(self.issue, self.user, '2nd comment 1st issue')
        third_comment = create_comment(second_issue, self.user, '1st comment 2nd issue')

        response = self.client.get(self.comment_by_issue_url)
        all_comments = response.context_data['comment_list']

        self.assertEqual(all_comments.count(), 2)

    def test_create_comment_POST(self):
        first_comment = create_comment(self.issue, self.user, '1st comment 1st issue')

        new_comment = {
            'author_id': 1,
            'description': 'New comment',
            'issues_id': 1
        }

        response_after_create = self.client.post(self.new_comment_url, new_comment)

        self.assertEqual(response_after_create.status_code, 200)

    def test_issue_log_GET(self):
        comment = create_comment(self.issue, self.user, 'New comment')
        create_comment_event(comment.pk)

        response = self.client.get(self.issue_log_url)
        response_context = response.context_data
        comment_events_objects = response_context['log_comment_events']
        issue_events_objects = response_context['log_issue_events']

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'uxhub/issue_log.html')

        self.assertTrue('log_issue_events' in response_context)
        self.assertTrue('log_comment_events' in response_context)
        self.assertEqual(comment_events_objects.count(), 1)
        self.assertEqual(issue_events_objects.count(), 1)


