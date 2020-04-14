from django.test import TestCase, Client

from uxhub.models import Commit, User, Project
from django.contrib.auth.models import User as AuthUser

SHA = "basesha"


class CommitViewsTest(TestCase):

    def setUp(self):
        self.johnAuthUser = self.mock_auth_user('john', 'john@gmail.com', 'john1234')
        self.john = self.mock_user('john', 'john@gmail.com', self.johnAuthUser)
        self.project = self.mock_project()
        self.commit = Commit.objects.create(comment="Foo", sha=SHA, branch="origin/master", github_id=51151,
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

    def test_commit_create(self):
        self.assertTrue(isinstance(self.commit, Commit))

    def test_commit_update(self):
        new_comment = "newcomment"
        commit = Commit.objects.get(sha=SHA)
        commit.comment = new_comment
        commit.save()
        self.assertEqual(commit.comment, new_comment)

    def test_commit_read(self):
        commit = Commit.objects.get(sha=SHA)
        self.assertIsNotNone(commit)
        self.assertEqual(SHA, commit.sha)

    def test_commit_delete(self):
        commit = Commit.objects.get(sha=SHA)
        commit.delete()
        self.assertIsNone(commit.id)
