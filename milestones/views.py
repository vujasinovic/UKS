# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from events.event_handling import create_milestone_event
from uxhub.models import Milestone


class MilestoneList(ListView):
    model = Milestone


class MilestoneView(DetailView):
    model = Milestone


class MilestoneCreate(CreateView):
    model = Milestone
    fields = ['name', 'start_date', 'end_date', 'projects']
    success_url = reverse_lazy('milestone_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_user = self.request.user
        create_milestone_event(self.object.pk, auth_user)
        return response


class MilestoneUpdate(UpdateView):
    model = Milestone
    fields = ['name', 'start_date', 'end_date', 'projects']
    success_url = reverse_lazy('milestone_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_user = self.request.user
        create_milestone_event(self.object.pk, auth_user)
        return response


class MilestoneDelete(DeleteView):
    model = Milestone
    success_url = reverse_lazy('milestone_list')
