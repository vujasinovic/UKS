from django.contrib.auth.models import User as AuthUser
from django.test import TestCase, Client


# Create your tests here.
from django.urls import reverse

from events.tests.test_utils import create_project, create_user, create_milestone, create_auth_user
from uxhub.models import Project


class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.milestone_id = 1
        self.milestone_log_url = reverse('events:milestone_log', kwargs={'pk': self.milestone_id})

        self.username = 'lukajvnv'
        self.password = 'Luka2903'
        self.invalid_password = 'blabla'

        self.auth_user = create_auth_user()
        self.user = create_user(self.auth_user)
        self.project = create_project(self.user)
        self.milestone = create_milestone(self.project)

    def test_login(self):
        correct_login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(correct_login, True)

        incorrect_login = self.client.login(username=self.username, password=self.invalid_password)
        self.assertEqual(incorrect_login, False)

    def test_milestone_log_login_required(self):
        response = self.client.get(self.milestone_log_url)
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.milestone_log_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'uxhub/milestone_log.html')
