from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from blogs.views import PostCreationView, PostDetailView, PostUpdateView

urlpatterns = patterns('',
    url(r'^new/?$', PostCreationView.as_view(), name='posts-create'),
    url(r'^posts/(?P<slug>.*?)/?$', PostDetailView.as_view(), name='posts-detail'),
    url(r'^update/(?P<slug>.*?)/?$', PostUpdateView.as_view(), name='posts-update'),
)