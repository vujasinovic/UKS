from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProjectList.as_view(), name='project_list'),
    path('view/<int:pk>', views.ProjectView.as_view(), name='project_view'),
    path('new', views.ProjectCreate.as_view(), name='project_new'),
    path('view/<int:pk>', views.ProjectView.as_view(), name='project_view'),
    path('edit/<int:pk>', views.ProjectUpdate.as_view(), name='project_edit'),
    path('delete/<int:pk>', views.ProjectDelete.as_view(), name='project_delete'),
]