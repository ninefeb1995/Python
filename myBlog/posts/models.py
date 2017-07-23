from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import pre_save


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    content = models.TextField()
    #slug = models.SlugField(unique=True, default="aaa")
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    image = models.ImageField(upload_to="image/", null=True, blank=True)
    publish = models.DateField(auto_now=False)
    draft = models.BooleanField(default=False)

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk': self.id})

    class Meta:
        ordering = ["-timestamp", ]

