from django.conf.urls import patterns, include, url
from users.views import RegisterView

urlpatterns = patterns('',
    url(r'^register/?$', RegisterView.as_view(template_name='users/register.html'), name='users-register'),
    url(r'^signin/?$', 'django.contrib.auth.views.login', {
            'template_name': 'users/sign_in.html'
        }, name='users-signin'),
    url(r'^signout/?$', 'django.contrib.auth.views.logout', {
            'template_name': 'users/signed_out.html'
        }, name='users-signout')
)
