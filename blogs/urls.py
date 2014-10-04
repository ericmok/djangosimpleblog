from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from blogs.views import PostCreationView
from blogs.views import PostDetailView
from blogs.views import PostUpdateView
from blogs.views import PostListView
from blogs.views import PostDeleteView

urlpatterns = patterns('',
    url(r'^new/?$', PostCreationView.as_view(), name='posts-create'),
    url(r'^/?$', PostListView.as_view(), name='posts-list'),
    url(r'^post/(?P<slug>.*?)/?$', PostDetailView.as_view(), name='posts-detail'),
    url(r'^update/(?P<slug>.*?)/?$', PostUpdateView.as_view(), name='posts-update'),
    url(r'^delete/(?P<slug>.*?)/?$', PostDeleteView.as_view(), name='posts-delete'),
)