from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from carts.models import Cart
from books.models import Book
import datetime
# Create your models here.

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('approved', 'Approved'),
    ('returned', 'Returned'),
)


class Order(models.Model):
    order_id = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(
        max_length=100, choices=ORDER_STATUS_CHOICES, default='created')
    cart = models.ForeignKey(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    begin_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField()

    def __str__(self):
        return str(self.cart.id)


# change book inventory based on order status
def order_pre_save(sender, instance, *args, **kwargs):
    new_status = instance.status
    cart = instance.cart
    cart_id = cart.id

    for record in Book.objects.raw("SELECT _book.id,_order.status as status,_item.id as item_id,_book.id as book_id,_book.title,_book.inventory, _item.quantity\
                                   FROM orders_order as _order join carts_cart as _cart join carts_cartitem as _item join books_book as _book\
                                   WHERE _order.cart_id=%s AND _item.item_id=_book.id;", [cart_id]):
        # Prevent same status
        if record.status != new_status:
            if new_status == 'approved':
                record.inventory -= record.quantity
            elif new_status == 'returned':
                record.inventory += record.quantity
            else:
                # Do nothing
                pass

        record.save()


pre_save.connect(order_pre_save, sender=Order)
