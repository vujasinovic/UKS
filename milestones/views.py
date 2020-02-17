# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from uxhub.models import Milestone


class MilestoneList(ListView):
    model = Milestone


class MilestoneView(DetailView):
    model = Milestone


class MilestoneCreate(CreateView):
    model = Milestone
    fields = ['name', 'start_date', 'end_date', 'projects']
    success_url = reverse_lazy('milestone_list')


class MilestoneUpdate(UpdateView):
    model = Milestone
    fields = ['name', 'start_date', 'end_date', 'projects']
    success_url = reverse_lazy('milestone_list')


class MilestoneDelete(DeleteView):
    model = Milestone
    success_url = reverse_lazy('milestone_list')
