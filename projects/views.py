from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from uxhub.models import Project


class ProjectList(ListView):
    model = Project


class ProjectView(DetailView):
    model = Project


class ProjectCreate(CreateView):
    model = Project
    fields = ['project_name', 'git_repository_url']
    success_url = reverse_lazy('project_list')


class ProjectUpdate(UpdateView):
    model = Project
    fields = ['project_name', 'git_repository_url']
    success_url = reverse_lazy('project_list')


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('project_list')


