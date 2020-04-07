from datetime import date

from django.contrib.auth.models import User as AuthUser
from django.test import TestCase, Client
from django.urls import reverse, resolve

from milestones.views import MilestoneList, MilestoneView, MilestoneUpdate, MilestoneCreate, MilestoneDelete
from uxhub.models import Milestone, Project, User

MILESTONE_NAME = 'MyMilestone'
NEW_MILESTONE_NAME = 'New milestone name'

PROJECT_NAME = 'MyProject'
GIT_REPOSITORY_URL = 'http://foo.bar'

EMAIL = 'john@mail.com'
USERNAME = 'john'


class MilestoneViewsTest(TestCase):
    client = Client()

    def setUp(self):
        self.milestone_list_url = reverse('milestone_list')
        self.milestone_view_url = reverse('milestone_view', args=[1])
        self.milestone_form_url = reverse('milestone_new')
        self.milestone_delete_url = reverse('milestone_delete', args=[1])

        self.johnAuthUser = self.mock_auth_user('john', 'john@gmail.com', 'pss')

        self.doeAuthUser = self.mock_auth_user('doe', 'doe@gmail.com', 'pss')

        self.john = self.mock_user('john', 'john@gmail.com', self.johnAuthUser)

        self.doe = self.mock_user('doe', 'doe@gmail.com', self.doeAuthUser)

        self.milestone = Milestone.objects.create(name=MILESTONE_NAME, projects=self.mock_project(),
                                                  start_date=date.today(),
                                                  end_date=date.today())
        self.milestone.save()

    def mock_auth_user(self, username, email, password):
        return AuthUser.objects.create_user(username, email, password)

    def mock_user(self, username, email, auth_user):
        return User.objects.create(username=username, email=email, auth_user=auth_user)

    def mock_project(self):
        return Project.objects.create(name=PROJECT_NAME,
                                      git_repository_url=GIT_REPOSITORY_URL,
                                      owner=self.john)

    def test_list(self):
        response = self.client.get(self.milestone_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(self.milestone_list_url).func.view_class, MilestoneList)
        self.assertTemplateUsed(response, 'uxhub/milestone_list.html')

    def test_view(self):
        self.client.get(self.milestone_view_url)
        self.assertEqual(resolve(self.milestone_view_url).func.view_class, MilestoneView)

    def test_new(self):
        url = reverse('milestone_new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func.view_class, MilestoneCreate)
        self.assertTemplateUsed(response, 'uxhub/milestone_form.html')

    def test_edit(self):
        url = reverse('milestone_edit', args=[1])
        self.client.get(url)
        self.assertEqual(resolve(url).func.view_class, MilestoneUpdate)

    def test_delete(self):
        url = reverse('milestone_delete', args=[1])
        self.client.get(url)
        self.assertEqual(resolve(url).func.view_class, MilestoneDelete)
