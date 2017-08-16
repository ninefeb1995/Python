from django.shortcuts import *
from django.template import loader
from django.http import *
from carts.models import *
from books.models import *
from orders.models import *
from datetime import datetime
from datetime import timedelta
from django.core.exceptions import *


def my_cart(request):
    """
    Showing book cart of every single client
    :param request: request GET cart from a client, it requires the client has to log in
    :return: render client's cart page or login page in the case of un-authenticating yet
    """
    categories = Category.objects.all()
    if request.user.is_authenticated:
        template = loader.get_template("cart/my_cart.html")
        try:
            user_id = request.user.id  # because of requiring clients log in, request has to contain id
            carts = Cart.objects.filter(user=user_id)  # every client has his/her cart
            status = {}
            books = []
            for key in request.COOKIES:  # due to we use cookie to store temporary cart, we get cart
                                                # info from COOKIE
                book_id = key.split('_')[0]
                if book_id.isdigit():
                    user_id_in_cache = request.COOKIES[key]
                    if user_id == int(user_id_in_cache):
                        try:
                            books.append(Book.objects.get(pk=int(book_id)))
                        except Book.DoesNotExist:
                            continue
            for cart in carts:
                try:
                    order = Order.objects.get(cart=cart.id)
                    status[cart.id] = order.status
                except ObjectDoesNotExist:
                    continue
            context = {
                'categories': categories,
                'carts': carts,
                'status': status,
                'books_in_cache': books,
            }
        except ObjectDoesNotExist:
            context = {}
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect(reverse('login'))


def add_to_cart(request):
    """
    Adding a book to temporary cart using COOKIE
    :param request: request "Add cart" from clients
    :return: it depends, if the book added is already exist or not, or in the case of un-authenticating
    """
    if request.user.is_authenticated:
        book_id = request.GET.get('book_id')
        key = str(book_id) + '_' + str(request.user.id)
        if key in request.COOKIES:
            return JsonResponse({
                'data': 'exist',
            })
        response = HttpResponse('added')
        response.set_cookie(key, request.user.id)
        return response
    else:
        return JsonResponse({
            'data': 'unauthenticated',
        })


def remove_from_cart(request):
    """
    Removing a book from temporary cart
    :param request: request "Delete" from clients
    :return: Rendering my-cart paging
    """
    user_id = request.user.id
    book_id = request.GET.get('book_id')
    key = str(book_id) + '_' + str(user_id)
    response = HttpResponseRedirect('/my-cart')
    response.delete_cookie(key)
    return response
