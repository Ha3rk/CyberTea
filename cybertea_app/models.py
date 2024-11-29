from django.db import models
from django.contrib.auth.models import User  # Import the User model
from django.utils.text import slugify  # Import slugify
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCount, HitCountMixin
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    image = models.ImageField(upload_to='imgs/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)  # Fix: Use the correct class name

    def __str__(self):
        return self.title


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Fixed User import
    fullname = models.CharField(max_length=40, blank=True)
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    bio = HTMLField()
    point = models.IntegerField(default=0)  # Fixed typo: integerField -> IntegerField
    profile_pic = ResizedImageField(size=[50, 80], quality=100, upload_to="authors", default=None, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Author, self).save(*args, **kwargs)  # Fix: Use the correct class name

    def __str__(self):
        return self.fullname


class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = HTMLField()
    categories = models.ManyToManyField(Category)
    date = models.DateTimeField(auto_now_add=True) 
    approved = models.BooleanField(default=False) 
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation') 
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs) 

    def __str__(self):
        return self.title
