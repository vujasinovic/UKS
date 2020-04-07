from django.test import SimpleTestCase
from django.urls import reverse, resolve
from projects.views import ProjectList, ProjectView, ProjectCreate, ProjectDelete, ProjectUpdate


class TestUrls(SimpleTestCase):

    def test_project_list_resolves(self):
        url = reverse('project_list')
        self.assertEqual(resolve(url).func.view_class, ProjectList)

    def test_project_view_resolves(self):
        url = reverse('project_view', args=[0])
        self.assertEqual(resolve(url).func.view_class, ProjectView)

    def test_project_new_resolves(self):
        url = reverse('project_new')
        self.assertEquals(resolve(url).func.view_class, ProjectCreate)

    def test_project_edit_resolves(self):
        url = reverse('project_edit', args=[0])
        self.assertEquals(resolve(url).func.view_class, ProjectUpdate)

    def test_project_delete_resolves(self):
        url = reverse('project_delete', args=[0])
        self.assertEquals(resolve(url).func.view_class, ProjectDelete)