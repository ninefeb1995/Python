from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from django.conf import settings
from django.dispatch import receiver
# Create your models here .


# define image uploaded location
def upload_image_to(instance, filename):
    title = instance.title
    slug = slugify(title)
    basename, file_extension = filename.split('.')
    return 'books/%s/%s.%s' % (slug, slug, file_extension)


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    condition = models.CharField(default='new', max_length=20, blank=True)
    publication_date = models.DateField(blank=True)
    language = models.CharField(max_length=50, blank=True)
    number_of_pages = models.PositiveIntegerField(blank=True)
    format = models.CharField(max_length=50, blank=True)
    authors = models.ManyToManyField('Author', blank=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', blank=True)
    inventory = models.PositiveIntegerField(blank=True)
    image = models.ImageField(upload_to=upload_image_to, max_length=500)
    archive_link = models.FileField(
        upload_to=None, editable=False, null=True, max_length=500)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_image_url(self):
        img = self.image
        if img:
            return img.image.url
        return img  # None

    def update_archive_link(self, address):
        self.archive_link = address
        self.save()


def create_archive_link(sender, instance, *args, **kwargs):
    # prevent infinite loop
    from books.serializers import BookSerializer
    from zipfile import ZipFile
    import json
    from random import randint

    post_save.disconnect(create_archive_link, sender=Book)

    # create request of testserver
    factory = APIRequestFactory()
    request = factory.get('/')
    # HyperlinkedModel need this
    serializer_context = {
        'request': Request(request),
    }

    book_serializer = BookSerializer(instance, context=serializer_context)

    image_uri = '%s/%s' % (settings.MEDIA_ROOT, instance.image.name)
    print(image_uri)
    slug = slugify(instance.title)
    archive_ext = 'zip'
    presentation_ext = 'json'
    image_ext = 'png'
    file_name = '%s/%s.%s' % (
        settings.ZIP_ROOT, slug, archive_ext)
    json_file = '%s/%s.%s' % (
        settings.ZIP_ROOT, slug, presentation_ext)

    # create json file
    with open(json_file, 'wb') as file_out:
        json_str = json.dumps(book_serializer.data) + "\n"
        json_bytes = json_str.encode('utf-8')
        file_out.write(json_bytes)

    # use zipfile to write json and image to archive
    with ZipFile(file_name, 'w') as file_out:
        file_out.write(json_file, slug + '.' + presentation_ext)
        file_out.write(image_uri, slug + '.' + image_ext)

    archive_link = '%s/%s.%s' % ('download', slug, archive_ext)
    instance.update_archive_link(archive_link)
    print(instance.archive_link.url)

    post_save.connect(create_archive_link, sender=Book)

post_save.connect(create_archive_link, sender=Book)


class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return '%d: %s' % (self.id, self.title)


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return '%d: %s' % (self.id, self.name)


class Publisher(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
