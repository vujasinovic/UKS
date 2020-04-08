from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User as AuthUser

from uxhub.models import Issue, Project, Milestone, User

ISSUE_NAME = 'IssueName'
NEW_ISSUE_NAME = 'New issue name'
ISSUE_DESCRIPTION = 'Issue description'

PROJECT_NAME = 'ProjectName'
GIT_REPOSITORY_URL = 'http://project'

EMAIL = 'john@mail.com'
USERNAME = 'john'

MILESTONE_NAME = 'MilestoneName'


class IssueTest(TestCase):

    def setUp(self):

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

    def test_issue_create(self):
        self.assertTrue(isinstance(self.issue, Issue))
        self.assertEqual(self.issue.__str__(), ISSUE_NAME)

    def test_issue_update(self):
        issue = Issue.objects.get(name=ISSUE_NAME)
        issue.name = NEW_ISSUE_NAME
        issue.save()
        self.assertEqual(issue.name, NEW_ISSUE_NAME)

    def test_issue_read(self):
        issue = Issue.objects.get(name=ISSUE_NAME)
        self.assertIsNotNone(issue)
        self.assertEqual(ISSUE_NAME, issue.name)

    def test_issue_delete(self):
        issue = Issue.objects.get(name=ISSUE_NAME)
        issue.delete()
        self.assertIsNone(issue.id)
