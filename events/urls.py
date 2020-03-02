from django.urls import path

from events import views

app_name = 'events'
urlpatterns = [
    path('comments', views.CommentList.as_view(), name='comment_list'),
    path('comments/issue_<int:issue_id>', views.CommentList.as_view(), name='comment_list_for_issue'),
    path('comments/view/<int:pk>', views.CommentView.as_view(), name='comment_detail'),
    path('comments/new', views.CommentCreate.as_view(), name='comment_new'),
    path('comments/edit/<int:pk>', views.CommentUpdate.as_view(), name='comment_update'),

    path('milestones_log/<int:pk>', views.MilestoneLogView.as_view(), name='milestone_log'),
    path('issue_log/<int:pk>', views.IssueLogView.as_view(), name='issue_log')

]
