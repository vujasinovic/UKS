from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from uxhub.models import Issue


class IssueList(ListView):
    model = Issue


class IssueView(DetailView):
    model = Issue


class IssueCreate(CreateView):
    model = Issue
    fields = ['name', 'description', 'project', 'milestones', 'start_date', 'end_date', 'approximated_time',
              'invested_time', 'completion']
    success_url = reverse_lazy('issue_list')


class IssueUpdate(UpdateView):
    model = Issue
    fields = ['name', 'description', 'project', 'milestones', 'start_date', 'end_date', 'approximated_time',
              'invested_time', 'completion']
    success_url = reverse_lazy('issue_list')


class IssueDelete(DeleteView):
    model = Issue
    success_url = reverse_lazy('issue_list')
