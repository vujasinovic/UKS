from django.urls import path

from . import views

urlpatterns = [
    path('', views.IssueList.as_view(), name='issue_list'),
    path('view/<int:pk>', views.IssueView.as_view(), name='issue_view'),
    path('new', views.IssueCreate.as_view(), name='issue_new'),
    path('view/<int:pk>', views.IssueView.as_view(), name='issue_view'),
    path('edit/<int:pk>', views.IssueUpdate.as_view(), name='issue_edit'),
    path('delete/<int:pk>', views.IssueDelete.as_view(), name='issue_delete'),
]
