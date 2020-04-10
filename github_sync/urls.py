from django.urls import path

from . import views

urlpatterns = [
    path('authorize', views.github_authorize, name='github_authorize'),
    path('projects', views.github_project_list, name='github_project_list'),
    path('import', views.github_project_import, name='github_project_import'),
]
