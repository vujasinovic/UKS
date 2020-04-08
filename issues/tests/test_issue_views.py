from datetime import date

from django.contrib.auth.models import User as AuthUser
from django.test import TestCase, Client
from django.urls import reverse, resolve

from issues.views import IssueCreate, IssueDelete, IssueList, IssueUpdate, IssueView
from uxhub.models import Issue, Milestone, Project, User

ISSUE_NAME = 'IssueName'
NEW_ISSUE_NAME = 'New issue name'
ISSUE_DESCRIPTION = 'Issue description'

PROJECT_NAME = 'ProjectName'
GIT_REPOSITORY_URL = 'http://project'

EMAIL = 'john@mail.com'
USERNAME = 'john'

MILESTONE_NAME = 'MilestoneName'


class IssueViewsTest(TestCase):
    client = Client()

    def setUp(self):
        self.issue_list_url = reverse('issue_list')
        self.issue_view_url = reverse('issue_view', args=[1])
        self.issue_form_url = reverse('issue_new')
        self.issue_delete_url = reverse('issue_delete', args=[1])

        self.johnAuthUser = self.mock_auth_user('john', 'john@gmail.com', 'john1234')
        self.john = self.mock_user('john', 'john@gmail.com', self.johnAuthUser)
        self.issue = Issue.objects.create(name=ISSUE_NAME, description=ISSUE_DESCRIPTION, project=self.mock_project(),
                                          milestones=self.mock_milestone(), start_date=date.today(),
                                          end_date=date.today(), approximated_time=2, invested_time=1, completion=False,
                                          state='OPEN')

        self.issue.save()

    def mock_auth_user(self, username, email, password):
        return AuthUser.objects.create_user(username, email, password)

    def mock_user(self, username, email, auth_user):
        return User.objects.create(username=username, email=email, auth_user=auth_user)

    def mock_project(self):
        return Project.objects.create(name=PROJECT_NAME,
                                      git_repository_url=GIT_REPOSITORY_URL,
                                      owner=self.john)

    def mock_milestone(self):
        return Milestone.objects.create(name=MILESTONE_NAME, projects=self.mock_project(), start_date=date.today(),
                                        end_date=date.today())

    def test_list(self):
        response = self.client.get(self.issue_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(self.issue_list_url).func.view_class, IssueList)
        self.assertTemplateUsed(response, 'uxhub/issue_list.html')

    def test_view(self):
        self.client.get(self.issue_view_url)
        self.assertEqual(resolve(self.issue_view_url).func.view_class, IssueView)

    def test_new(self):
        url = reverse('issue_new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func.view_class, IssueCreate)
        self.assertTemplateUsed(response, 'uxhub/issue_form.html')

    def test_edit(self):
        url = reverse('issue_edit', args=[1])
        self.client.get(url)
        self.assertEqual(resolve(url).func.view_class, IssueUpdate)

    def test_delete(self):
        url = reverse('issue_delete', args=[1])
        self.client.get(url)
        self.assertEqual(resolve(url).func.view_class, IssueDelete)