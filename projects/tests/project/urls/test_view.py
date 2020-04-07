from django.urls import reverse
from uxhub.models import Project, User
from django.test import TestCase, Client
from django.contrib.auth.models import User as AuthUser
import json

class TestProjectView(TestCase):

    def setUp(self):
        self.client = Client()
        self.project_list_url = reverse('project_list')
        self.project_view_url = reverse('project_view', args=[1])
        self.project_form_url = reverse('project_new')
        self.project_delete_url = reverse('project_delete', args=[1])

        self.authUser2 = self.authUser = AuthUser.objects.create_user(
            'viktor2', 'viktor@gmail.com', 'pss')

        self.authUser1 = AuthUser.objects.create_user(
            'viktor1', 'viktor@gmail.com', 'pss')

        self.user1 = User.objects.create(
            username="pera",
            email="pera@gmail.com",
            auth_user=self.authUser1
        )

        self.user2 = User.objects.create(
            username="mika",
            email="mika@gmail.com",
            auth_user=self.authUser2
        )

        self.project1 = Project.objects.create(
            name="projekatBend",
            git_repository_url="perod",
            owner=self.user2
        )

        self.project1.save()

    def test_project_list(self):
        response = self.client.get(self.project_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'uxhub/project_list.html')

    def test_project_detail(self):
        response = self.client.get(self.project_view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'uxhub/project_detail.html')

    def test_project_form(self):
        response = self.client.get(self.project_form_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'uxhub/project_form.html')

    def test_project_delete(self):
        response = self.client.get(self.project_delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'uxhub/project_confirm_delete.html')



