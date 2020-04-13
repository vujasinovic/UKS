from django.test import TestCase

# Create your tests here.
from events.custom_form import CommentForm, CommentFormTest
from events.tests.test_utils import create_auth_user, create_user, create_project, create_milestone, create_issue


class TestForms(TestCase):
    def setUp(self):
        self.auth_user = create_auth_user()
        self.user = create_user(self.auth_user)
        self.project = create_project(self.user)
        self.milestone = create_milestone(self.project)
        self.issue = create_issue(self.project, self.milestone)

    def test_new_comment_form_valid(self):
        form = CommentFormTest({
            'description': 'Comment',
            'author': 1,
            'issues': 1,
        })
        self.assertTrue(form.is_valid())

    def test_new_comment_form_invalid(self):
        form = CommentFormTest(data={
            'description': 'Comment'
        })

        self.assertFalse(form.is_valid())

        # fields author and issues are required
        errors = form.errors
        self.assertTrue('author' in errors)
        self.assertTrue('issues' in errors)



