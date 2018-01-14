from django.db import models
from django.conf import settings
from books.models import Book



class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    items = models.ManyToManyField(Book, through='CartItem')

    def __str__(self):
        return self.user.username + str(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey('Cart')
    item = models.ForeignKey(Book)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.item.title