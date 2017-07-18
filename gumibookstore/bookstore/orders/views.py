from orders.models import Order
from orders.serializers import OrderSerializer
from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import *
from django.template import loader
from django.http import *
from carts.models import *
from books.models import *
from orders.models import *
from datetime import datetime
from datetime import timedelta


# Create your views here.


class OrderViewSet(viewsets.ModelViewSet):
    """
    This viewset auto provides `list`, `retrieve`, `create`, `update`
    and destroy actions.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # define allowed methods
    http_method_names = ['get', 'put', 'head']


def borrow(request):
    """
    Adding a temporary cart from COOKIES to database
    :param request: request "Borrow" of clients
    :return: my cart page redering
    """
    user_id = request.user.id  # id of user requesting to borrow books
    response = HttpResponseRedirect('/my-cart')
    books_to_borrow = request.GET.getlist('books_check_out')
    if books_to_borrow:
        new_cart = Cart.objects.create(user=request.user)
        new_cart.save()
        for book in books_to_borrow:
            key = str(book) + '_' + str(user_id)
            response.delete_cookie(key)
            get_book = Book.objects.get(pk=book)
            new_cart_item = CartItem.objects.create(cart=new_cart, item=get_book)
            get_book.inventory -= 1
            get_book.save()
            new_cart_item.save()
        start_day = datetime.now()
        end_day = start_day + timedelta(days=14)  # We limit the number of borrowing days is 14 from the day
        # they create order
        new_order = Order.objects.create(order_id=user_id,
                                         cart=new_cart,
                                         user=request.user,
                                         begin_date=start_day,
                                         end_date=end_day)
        new_order.save()
    return response
