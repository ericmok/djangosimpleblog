from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^create/?$', TemplateView.as_view(template_name='blogs/posts_create.html'), name='posts-create'),
)
