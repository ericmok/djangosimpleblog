from django.db import models, IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.template.defaultfilters import slugify


POSTABLE_MODELS = ('Edition', 'Quote')

def get_model_class(name):
    return {'Edition': Edition, 'Quote': Quote}[name]


class AbstractDateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PostManager(models.Manager):

    def create_with_edition(self, title, author, text):
        """
        Create a new post and new edition. Slug is auto genereated
        """
        new_post = Post.objects.create(title=title, slug=slugify(title), author=author)
        new_edition = Edition.objects.create(post=new_post, text=text)
        return new_post


class Post(models.Model):
    reference_type = models.CharField(max_length=16, choices=POSTABLE_MODELS, null=True, blank=True, default=None)
    reference_id = models.PositiveIntegerField()

    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    objects = PostManager()

    tags = models.ManyToManyField('Tag')

    def get_text(self):
        return self.title

    def set_reference(self, reference_model):
        if reference_model.__class__.__name__ in POSTABLE_MODELS:
            self.reference_type = reference_model.__class__.__name__
            self.reference_id = reference_model.id

    def set_reference(self, reference_type, reference_id):
        if reference_type in POSTABLE_MODELS:
            try:
                existence_check = get_model_class(reference_type).objects.get(pk=reference_id)
                self.reference_type = reference_type
                self.reference_id = reference_id
            except:
                raise IntegrityError('Reference does not exist')

    def get_reference(self):
        if self.reference_type not in POSTABLE_MODELS:
            return None
        else:
            try:
                reference_model = get_model_class(self.reference_type).objects.get(pk=self.reference_id)
                return reference_model
            except DoesNotExist:
                return None


class Edition(models.Model):
    post = models.ForeignKey('Post')
    text = models.TextField()

    def get_text(self):
        return self.text


class Quote(models.Model):
    edition = models.ForeignKey('Edition')
    start = models.IntegerField()
    end = models.IntegerField()
    order = models.IntegerField()

    class Meta:
        ordering = ['order']


class Tag(models.Model):
    name = models.CharField(max_length=128)