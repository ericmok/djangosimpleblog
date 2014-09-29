from django.shortcuts import render
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from braces.views import LoginRequiredMixin

from .forms import PostModelForm


class PostCreationView(View):
    form_class = PostModelForm
    template_name = 'blogs/posts_create.html'

    def get(self, request, *args, **kwargs):
        form = PostModelForm()
        return render(request, self.template_name, {'form': form})