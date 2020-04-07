from django.test import TestCase
from uxhub.models import Project, User
from django.contrib.auth.models import User as AuthUser


# Create your tests here.

class ProjectTest(TestCase):

    def setUp(self):

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

    def create_project(self, name="prddfsdf", git_repository_url="pero.com"):
        return Project.objects.create(
            name=name,
            git_repository_url=git_repository_url,
            owner=self.user1
        )

    def test_project_creation(self):
        w = self.create_project()
        p = self.project1
        self.assertNotEqual(w.owner, p.owner)
        self.assertTrue(isinstance(w, Project))
        self.assertNotEqual(w.name, p.name)
        self.assertEqual(w.git_repository_url, "pero.com")

    def test_project_update(self):
        proj = Project.objects.get(pk = self.project1.pk)
        old_name = proj.name

        proj.name = 'novo_ime'

        self.assertNotEqual(old_name,proj.name)

    def test_project_delete(self):
        count_before_delete = Project.objects.count()
        self.project1.delete()

        count_after_delete = Project.objects.count()

        self.assertNotEqual(count_before_delete, count_after_delete)



