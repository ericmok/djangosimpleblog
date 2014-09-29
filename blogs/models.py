from django.db import models, IntegrityError, transaction
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.template.defaultfilters import slugify


class AbstractDateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-modified_at']


class PostManager(models.Manager):

    def create_with_edition(self, title, author, text):
        """
        Create a new post and new edition. Slug is auto genereated
        """
        new_post = Post.objects.create(title=title, slug=slugify(title), author=author)
        new_edition = Edition.objects.create(post=new_post, text=text)
        return new_post


class Post(AbstractDateModel):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    objects = PostManager()

    tags = models.ManyToManyField('Tag')

    def get_text(self):
        return self.title

    def generate_unique_slug(self):
        new_slug = slugify(self.title)
        counter = 0
        while (Post.objects.filter(slug=new_slug).count() > 0):
            new_slug = slugify('%s%s' % (counter, self.title))
            counter += 1

        self.slug = new_slug
        return new_slug

    def save(self, **kwargs):
        with transaction.atomic():
            self.generate_unique_slug()
            super(Post, self).save(**kwargs)


class Edition(AbstractDateModel):
    post = models.ForeignKey('Post', related_name='editions')
    text = models.TextField()

    def get_text(self):
        return self.text


class Tag(models.Model):
    name = models.CharField(max_length=128)