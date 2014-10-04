from django import forms

from blogs.models import Post, Edition


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title',)


class PostCreationForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(max_length=16383, widget=forms.Textarea)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(PostCreationForm, self).__init__(*args, **kwargs)

    def save(self):
        title = self.cleaned_data['title']
        author = self.request.user
        text = self.cleaned_data['text']
        return Post.objects.create_with_edition(title=title, author=author, text=text)


class PostUpdateForm(forms.Form):
    text = forms.CharField(max_length=16383, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(PostUpdateForm, self).__init__(*args, **kwargs)

    def save(self, instance=None):
        post_instance = instance or self.instance
        text = self.cleaned_data['text']
        new_edition = Edition.objects.create(post=post_instance, text=text)
        return post_instance