from django import forms

from blogs.models import Post, Edition


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title',)