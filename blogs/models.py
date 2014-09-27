from django.db import models, IntegrityError, transaction
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.template.defaultfilters import slugify


POSTABLE_MODEL_CHOICES = (('Edition', 'Edition'), ('Quote', 'Quote'))
POSTABLE_MODEL_NAMES = [p[0] for p in POSTABLE_MODEL_CHOICES]

def get_model_class(name):
    return {'Edition': Edition, 'Quote': Quote}[name]


class AbstractDateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['modified_at']


class PostManager(models.Manager):

    def create_with_edition(self, title, author, text):
        """
        Create a new post and new edition. Slug is auto genereated
        """
        new_post = Post.objects.create(title=title, slug=slugify(title), author=author)
        new_edition = Edition.objects.create(post=new_post, text=text)
        return new_post


class Post(AbstractDateModel):
    reference_type = models.CharField(max_length=16, choices=POSTABLE_MODEL_CHOICES, null=True, blank=True, default=None)
    reference_id = models.PositiveIntegerField(null=True, blank=True)

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

    def set_reference_from_model(self, reference_model):
        if reference_model.__class__.__name__ in POSTABLE_MODEL_NAMES:
            self.reference_type = reference_model.__class__.__name__
            self.reference_id = reference_model.id
        else:
            raise ValueError('reference_type must be in POSTABLE_MODEL_CHOICES')

    def set_reference_from_type_and_id(self, reference_type, reference_id):
        if reference_type in POSTABLE_MODEL_NAMES:
            try:
                existence_check = get_model_class(reference_type).objects.get(pk=reference_id)
                self.reference_type = reference_type
                self.reference_id = reference_id
            except:
                raise IntegrityError('Reference does not exist')
        else:
            raise ValueError('reference_type must be in POSTABLE_MODEL_CHOICES')

    def get_reference(self):
        if self.reference_type not in POSTABLE_MODEL_CHOICES:
            raise ValueError('reference_type must be in POSTABLE_MODEL_CHOICES')
        else:
            try:
                reference_model = get_model_class(self.reference_type).objects.get(pk=self.reference_id)
                return reference_model
            except DoesNotExist:
                raise IntegrityError('Reference does not exist')

    def save(self, **kwargs):
        with transaction.atomic():
            self.generate_unique_slug()
            super(Post, self).save(**kwargs)


class Edition(AbstractDateModel):
    post = models.ForeignKey('Post', related_name='editions')
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