from django import forms

from blogs.models import Post, Edition


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title',)


class PostCreationForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(max_length=16383)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request

    def save(self):
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        Post.objects.create_with_edition(title=title, author=request.user, text=text)