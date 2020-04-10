from django.urls import path

from . import views

urlpatterns = [
    path('', views.commit_list, name='commit_list'),
]
