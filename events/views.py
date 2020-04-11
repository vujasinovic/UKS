# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from events import metrics
from events.custom_form import CommentForm
from events.event_handling import create_comment_event
from uxhub.models import Comment, Milestone, ChangingMilestone, Issue, ChangingIssue, ChangingComment, User


class CommentList(LoginRequiredMixin, ListView):
    model = Comment

    def get_queryset(self):
        try:
            issue_id = self.kwargs['issue_id']
            ret = Comment.objects.filter(issues__pk=issue_id)
        except KeyError:
            ret = Comment.objects.all()
        return ret

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        issue_id = self.kwargs.get('issue_id', False)
        if issue_id:
            context['issue_id'] = issue_id
        # else:
        #     context['issue_id'] = -1
        return context


class CommentView(DetailView):
    model = Comment


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    form_class.base_fields['issues'].disabled = True

    def get_initial(self):
        try:
            pk = self.kwargs['issue_id']
            auth_user = self.request.user
            author = None
            if auth_user.is_authenticated:
                author = User.objects.get(auth_user=auth_user)
        except KeyError:
            return super().get_initial()
        else:
            issue = Issue.objects.get(pk=pk)
            return {
                'issues': issue,
                'author': author
            }

    def form_valid(self, form):
        response = super().form_valid(form)
        create_comment_event(self.object.pk)
        return response

    def get_success_url(self):
        if self.object.issues.pk:
            return reverse_lazy('events:issue_log', kwargs={'pk': self.object.issues.pk})
        else:
            return reverse_lazy('events:comment_list_for_issue', kwargs={'issue_id': self.object.issues.pk})


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    # success_url = reverse_lazy('events:comment_list')

    def get_initial(self):
        auth_user = self.request.user
        logged_author = User.objects.get(auth_user=auth_user)
        comment_author = self.object.author
        if logged_author.id != comment_author.id:
            raise Http404("You dont have rights to edit comment!")

        pk = self.object.issues.pk
        issue = Issue.objects.get(pk=pk)
        return {
            'issues': issue,
            'author': comment_author
        }

    def form_valid(self, form):
        response = super().form_valid(form)
        create_comment_event(self.object.pk)
        return response

    def get_success_url(self):
        redirect_to_logs = self.request.GET.get('backToLogs', False)
        redirect_to_detail = self.request.GET.get('backToDetail', False)
        if redirect_to_logs:
            return reverse_lazy('events:issue_log', kwargs={'pk': self.object.issues.pk})
        elif redirect_to_detail:
            return reverse_lazy('events:comment_detail', kwargs={'pk': self.object.pk})
        else:
            return reverse_lazy('events:comment_list_for_issue', kwargs={'issue_id': self.object.issues.pk})


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
