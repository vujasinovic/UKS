from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from events.event_handling import create_issue_event
from uxhub.models import Issue


class IssueList(ListView):
    model = Issue


class IssueView(DetailView):
    model = Issue


class IssueCreate(CreateView):
    model = Issue
    fields = ['name', 'description', 'project', 'milestones', 'start_date', 'end_date', 'approximated_time',
              'invested_time', 'completion', 'state', 'assignee']
    success_url = reverse_lazy('issue_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_user = self.request.user
        create_issue_event(self.object.pk, auth_user)
        return response


class IssueUpdate(UpdateView):
    model = Issue
    fields = ['name', 'description', 'project', 'milestones', 'start_date', 'end_date', 'approximated_time',
              'invested_time', 'completion', 'state', 'assignee']
    success_url = reverse_lazy('issue_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_user = self.request.user
        create_issue_event(self.object.pk, auth_user)
        return response


class IssueDelete(DeleteView):
    model = Issue
    success_url = reverse_lazy('issue_list')
