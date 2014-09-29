from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.urlresolvers import reverse_lazy, reverse

from braces.views import LoginRequiredMixin

from .forms import PostModelForm, PostCreationForm
from .models import Post, Edition


class PostCreationView(View):
    form_class = PostModelForm
    template_name = 'blogs/posts_create.html'

    def get(self, request, *args, **kwargs):
        form = PostCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PostCreationForm(request, request.POST)
        if form.is_valid():
            new_post = form.save()
            return redirect(reverse('posts-detail', kwargs={'slug': new_post.slug}))
        else:
            return render(request, self.template_name, {'form': form})


class PostDetailView(View):
    template_name = 'blogs/posts_detail.html'

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        if slug:
            try:
                post = Post.objects.select_related('editions').get(slug=slug)
                context = {
                    'post': post
                }
                return render(request, self.template_name, context)
            except Post.DoesNotExist:
                raise Http404
        else:
            raise Http404