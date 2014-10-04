from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.views import redirect_to_login

from braces.views import LoginRequiredMixin, UserPassesTestMixin

from .forms import PostModelForm, PostCreationForm, PostUpdateForm
from .models import Post, Edition


class PostCreationView(LoginRequiredMixin, View):
    form_class = PostModelForm
    login_url = reverse_lazy('users-signin')
    template_name = 'blogs/posts_create.html'
    paginate_by = 2

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


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blogs/posts_list.html'
    paginate_by = 24


class PostDetailView(DetailView):
    template_name = 'blogs/posts_detail.html'
    context_object_name = 'post'
    model = Post
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['posts'] = self.model.objects.all()[:16]
        return context

    def get_object(self):
        try:
            return self.model.objects.select_related('editions').get(slug=self.kwargs[self.slug_field])
        except Post.DoesNotExist:
            raise Http404


class PostUpdateView(UserPassesTestMixin, View):
    template_name = 'blogs/posts_update.html'
    form_class = PostUpdateForm
    login_url = reverse_lazy('users-signin')

    # Raise exception if test func fails
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        # See: https://github.com/brack3t/django-braces/issues/88
        if not request.user.is_authenticated():
            # Redirect
            return redirect_to_login(request.get_full_path(),
                                     self.get_login_url(),
                                     self.get_redirect_field_name())
        return super(PostUpdateView, self).dispatch(request, *args, **kwargs)

    def test_func(self, user):
        slug = self.kwargs.get('slug', None)

        if slug:
            post = get_object_or_404(Post, slug=slug)
            if post.author == user:
                return True
            else:
                return False
        else:
            raise Http404

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