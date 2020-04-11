from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from uxhub.models import User


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_user = form.instance
        User.objects.create(username=auth_user.username, email=auth_user.email, auth_user=auth_user)
        return response
