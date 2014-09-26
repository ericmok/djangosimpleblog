from django.conf.urls import patterns, include, url
from users.views import RegisterView

urlpatterns = patterns('',
    url(r'^register/?$', RegisterView.as_view(template_name='users/register.html'), name='users-register'),
)
