from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from blogs.views import PostCreationView

urlpatterns = patterns('',
    url(r'^create/?$', PostCreationView.as_view(), name='posts-create'),
)
