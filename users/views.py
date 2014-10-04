from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView

from users.forms import RegisterForm


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('posts-list')

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)