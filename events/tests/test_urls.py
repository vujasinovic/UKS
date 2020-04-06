from django.test import TestCase


# Create your tests here.
from django.urls import reverse, resolve, exceptions, NoReverseMatch

from events.views import CommentList


class TestUrls(TestCase):
    def setUp(self):
        self.comment_list_path_name = 'events:comment_list'
        self.comment_list_by_issue_path_name = 'events:comment_list_for_issue'
        self.issue_id = 1
        self.invalid_issue_id = 'a'

    def test_comment_list(self):
        url = reverse(self.comment_list_path_name)

        self.assertEqual(resolve(url).func.view_class, CommentList)

    def test_comment_list_for_issue(self):
        url = reverse(self.comment_list_by_issue_path_name, args=[self.issue_id])

        self.assertEqual(resolve(url).view_name, self.comment_list_by_issue_path_name)
        self.assertEqual(resolve(url).func.view_class, CommentList)

    def test_comment_list_for_issue_invalid_args(self):
        with self.assertRaises(NoReverseMatch) as cm:
            url = reverse(self.comment_list_by_issue_path_name, args=[self.invalid_issue_id])
