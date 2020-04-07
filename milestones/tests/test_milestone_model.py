from datetime import date

from django.contrib.auth.models import User as AuthUser
from django.test import TestCase

from uxhub.models import Milestone, Project, User

MILESTONE_NAME = 'MyMilestone'
NEW_MILESTONE_NAME = 'New milestone name'

PROJECT_NAME = 'MyProject'
GIT_REPOSITORY_URL = 'http://foo.bar'

EMAIL = 'john@mail.com'
USERNAME = 'john'


class MilestoneTest(TestCase):

    def setUp(self):
        self.milestone = self.create_milestone()

    @staticmethod
    def mock_auth_user():
        return AuthUser.objects.create()

    def mock_uxhub_user(self):
        return User.objects.create(username=USERNAME, email=EMAIL, auth_user=self.mock_auth_user())

    def mock_uxhub_project(self):
        return Project.objects.create(name=PROJECT_NAME, git_repository_url=GIT_REPOSITORY_URL,
                                      owner=self.mock_uxhub_user())

    def test_milestone_create(self):
        self.assertTrue(isinstance(self.milestone, Milestone))
        self.assertEqual(self.milestone.__str__(), MILESTONE_NAME)

    def test_milestone_update(self):
        milestone = Milestone.objects.get(name=MILESTONE_NAME)
        milestone.name = NEW_MILESTONE_NAME
        milestone.save()
        self.assertEqual(milestone.name, NEW_MILESTONE_NAME)

    def test_milestone_read(self):
        milestone = Milestone.objects.get(name=MILESTONE_NAME)
        self.assertIsNotNone(milestone)
        self.assertEqual(MILESTONE_NAME, milestone.name)

    def test_milestone_delete(self):
        milestone = Milestone.objects.get(name=MILESTONE_NAME)
        milestone.delete()
        self.assertIsNone(milestone.id)

    def create_milestone(self):
        return Milestone.objects.create(name=MILESTONE_NAME, projects=self.mock_uxhub_project(),
                                        start_date=date.today(),
                                        end_date=date.today())
