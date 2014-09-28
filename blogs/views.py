from django.shortcuts import render
from django.conf import settings
from django.views.generic import FormView

from braces import LoginRequiredMixin

class PostCreationView(LoginRequiredMixin, FormView):
    template_name = 'blogs/posts_create.html'
    login_url = settings.LOGIN_URL