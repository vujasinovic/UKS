from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from events import metrics
from events.custom_form import CommentForm
from uxhub.models import Comment, Milestone, ChangingMilestone, Issue, ChangingIssue, ChangingComment


class CommentList(LoginRequiredMixin, ListView):
    model = Comment

    def get_queryset(self):
        try:
            issue_id = self.kwargs['issue_id']
            ret = Comment.objects.filter(issues__pk=issue_id)
        except KeyError:
            ret = Comment.objects.all()
        return ret


class CommentView(DetailView):
    model = Comment


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy('events:comment_list')


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy('events:comment_list')


class MilestoneLogView(LoginRequiredMixin, DetailView):
    model = Milestone
    template_name = "uxhub/milestone_log.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        milestone_id = self.kwargs['pk']
        context['log_events'] = ChangingMilestone.objects.filter(milestones__id=milestone_id).order_by('-time')
        return context


class IssueLogView(LoginRequiredMixin, DetailView):
    model = Issue
    template_name = "uxhub/issue_log.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        issue_id = self.kwargs['pk']
        context['log_issue_events'] = ChangingIssue.objects.filter(issues__id=issue_id).order_by('-time')
        context['log_comment_events'] = ChangingComment.objects.filter(issues__id=issue_id).order_by('-time')
        return context
