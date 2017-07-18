from rest_framework import serializers
from books.models import Book, Author, Category, Publisher
from django.contrib.auth.models import User


class CategorySerializer(serializers.RelatedField):

    class Meta:
        model = Category
        fields = ('title',)

    def to_representation(self, value):
        return '%s' % (value.title)


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = ('id', 'name',)

    def to_representation(self, value):
        return '%s' % (value.name)


class BookSerializer(serializers.HyperlinkedModelSerializer):
    publisher = serializers.StringRelatedField()
    publisher_id = serializers.PrimaryKeyRelatedField(
        queryset=Publisher.objects.all(), source='publisher', write_only=True)
    authors = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Author.objects.all()
    )
    categories = serializers.SlugRelatedField(
        many=True,
        slug_field='title',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Book
        fields = ('url', 'id', 'title', 'publisher_id', 'publisher',
                  'authors', 'categories', 'publication_date',
                  'language', 'number_of_pages', 'format',
                  'inventory', 'description', 'condition',
                  'image', 'archive_link')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'id', 'username')
