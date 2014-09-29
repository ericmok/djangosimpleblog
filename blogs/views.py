from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.urlresolvers import reverse_lazy, reverse

from braces.views import LoginRequiredMixin

from .forms import PostModelForm, PostCreationForm, PostUpdateForm
from .models import Post, Edition


class PostCreationView(LoginRequiredMixin, View):
    form_class = PostModelForm
    login_url = reverse_lazy('users-signin')
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


class PostUpdateView(View):
    template_name = 'blogs/posts_update.html'
    form_class = PostUpdateForm    

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        if slug:
            post = get_object_or_404(Post, slug=slug)
            form = self.form_class()
            context = {'post': post, 'form': form}
            return render(request, self.template_name, context)
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        if slug:
            post = get_object_or_404(Post, slug=slug)
            form = self.form_class(request.POST)
            context = {'post': post, 'form': form}

            if form.is_valid():
                form.save(post_instance=post)
                return redirect(reverse('posts-detail', kwargs={'slug': post.slug}))
            else:
                return render(request, self.template_name, context)
        else:
            raise Http404