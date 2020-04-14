from django.contrib.auth.models import User as AuthUser
from django.test import TestCase, Client
from django.urls import reverse

from uxhub.models import Project, User, Commit


class IssueViewsTest(TestCase):
    client = Client()

    def setUp(self):
        self.commit_list_url = reverse('commit_list')

        self.johnAuthUser = self.mock_auth_user('john', 'john@gmail.com', 'john1234')
        self.john = self.mock_user('john', 'john@gmail.com', self.johnAuthUser)
        self.project = self.mock_project()
        self.commit = Commit.objects.create(comment="Foo", sha="exampelsha", branch="origin/master", github_id=51151,
                                            projects=self.project, author=self.john)
        self.commit.save()

    def mock_auth_user(self, username, email, password):
        return AuthUser.objects.create_user(username, email, password)

    def mock_user(self, username, email, auth_user):
        return User.objects.create(username=username, email=email, auth_user=auth_user)

    def mock_project(self):
        return Project.objects.create(name="Project",
                                      git_repository_url="https://github.com/user/Project",
                                      owner=self.john)

    def test_list(self):
        response = self.client.get(self.commit_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'uxhub/commit_list.html')
        self.assertTrue(self.commit.sha in str(response.content))
