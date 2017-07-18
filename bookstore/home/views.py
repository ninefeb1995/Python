from django.shortcuts import *
from django.template import loader
from django.http import *
from home import models
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.exceptions import *


categories = models.Category.objects.all()


def index(request):
    featuredbooks = models.Book.objects.filter(book_is_new=False)
    newbooks = models.Book.objects.filter(book_is_new=True)
    context = {
        'featuredbooks': featuredbooks,
        'newbooks': newbooks,
        'categories': categories,
    }
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render(context, request))


def category(request, cate_id):
    books_by_cate = models.Book.objects.filter(cate_id=cate_id)
    get_cate = models.Category.objects.get(id=cate_id)
    template = loader.get_template('home/category.html')
    paginator = Paginator(books_by_cate, 9)
    current_pagenumber = request.GET.get('currentpage')
    try:
        quantity_of_books_per_page = paginator.page(current_pagenumber)
    except EmptyPage:
        quantity_of_books_per_page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        quantity_of_books_per_page = paginator.page(1)  # Maybe redirect to 404 not found page
    context = {'categories': categories,
               'cate': get_cate,
               'quantity_of_books_per_page': quantity_of_books_per_page,
               }
    return HttpResponse(template.render(context, request))


def autobook(request):
    auto_books = models.Book.objects.all()
    template = loader.get_template('home/autobook.html')
    paginator = Paginator(auto_books, 9)
    current_pagenumber = request.GET.get('currentpage')
    try:
        quantity_of_books_per_page = paginator.page(current_pagenumber)
    except EmptyPage:
        quantity_of_books_per_page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        quantity_of_books_per_page = paginator.page(1)  # Maybe redirect to 404 not found page
    context = {
                'categories': categories,
                'quantity_of_books_per_page': quantity_of_books_per_page,
            }
    return HttpResponse(template.render(context, request))


def register(request):
    template = loader.get_template('home/register.html')
    return HttpResponse(template.render({}, request))




def myaccount(request):
    content = request.POST
    template = loader.get_template('home/myaccount.html')
    context = {'categories': categories, }
    username = content.get('username')
    password = content.get('password')
    if username and password:
        user = authenticate(username=username, password=password)
        if not user:
            context = {'validator': "**Login information is not valid",
                       'categories': categories,
                       'username': username,
                       'password': password
                       }
            return HttpResponse(template.render(context, request))
        else:
            login(request, user)
            if user.is_superuser:
                pass
                # return HttpResponseRedirect(reverse('managepage'))
            else:
                return index(request)
    return HttpResponse(template.render(context, request))


def logout_(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next'))


def contact(request):
    content = request.POST
    template = loader.get_template('home/contact.html')
    context = {'is_sent': 'false',
               'categories': categories,
               }
    if not content.get('email') is None:
        subject = str(content['email']) + "_" + str(datetime.today())
        message = content['name'] + '\n' + \
                  content['phone'] + '\n' + \
                  content['message'] + '\n'
        send_mail(
            subject,
            str(message),
            str(content['email']),
            [settings.EMAIL_HOST_USER],
            fail_silently=True,
        )
        context = {'is_sent': 'true',
                   'categories': categories,
                   }
        # return HttpResponseRedirect(reverse('index'))

    return HttpResponse(template.render(context, request))


def detail(request, book_id):
    template = loader.get_template("home/detail.html")
    try:
        get_book = models.Book.objects.get(pk=book_id)
        get_cate = get_book.cate_id
        get_list_book_of_cate = models.Book.objects.filter(cate_id=get_cate)
    except models.Book.DoesNotExist:
        raise Http404("Book is not exist...!")
    else:
        context = {
            'book': get_book,
            'list_book_of_cate': get_list_book_of_cate,
            'categories': categories,
        }
    return HttpResponse(template.render(context, request))


def mycart(request):
    if request.user.is_authenticated:
        template = loader.get_template("home/mycart.html")
        try:
            user_id = request.user.id
            order = models.Order.objects.get(user_id=user_id)
            order_details = models.OrderDetail.objects.filter(order_id=order.id)
            context = {
                'order_details': order_details,
            }
        except ObjectDoesNotExist:
            context = {}
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect(reverse('myaccount'))


# def get(self, request, *args, **kwargs):
#     cart = self.get_object()
#     item_id = request.GET.get('item')
#     delete_item = request.GET.get('delete', False)
#     flash_msg = ''
#     item_added = False
#
#     if item_id:
#         item_instance = get_object_or_404(Variation, id=item_id)
#         qty = request.GET.get("qty", 1)
#         try:
#             if int(qty) < 1:
#                 delete_item = True
#         except:
#             raise Http404
#
#         cart_item, created = CartItem.objects.get_or_create(
#             cart=cart, item=item_instance)
#         if created:
#             flash_msg = 'Đã thêm sản phẩm vào giỏ.'
#             item_added = True
#         if delete_item:
#             flash_msg = 'Đã xóa sản phẩm khỏi giỏ.'
#             cart_item.delete()
#         else:
#             if not created:
#                 flash_msg = 'Số lượng sản phẩm đã được cập nhật.'
#             cart_item.quantity = qty
#             cart_item.save()
#         if not request.is_ajax():
#             return HttpResponseRedirect(reverse('cart'))
#             # return cart_item.cart.get_absolute_url()
#
#     if request.is_ajax():
#         try:
#             total = cart_item.line_item_total
#             print(total)
#         except:
#             total = None
#         try:
#             subtotal = cart_item.cart.subtotal
#         except:
#             subtotal = None
#         try:
#             tax_total = cart_item.cart.tax_total
#         except:
#             tax_total = None
#         try:
#             cart_total = cart_item.cart.total
#         except:
#             cart_total = None
#         try:
#             total_items = cart_item.cart.itemList.count()
#         except:
#             total_items = 0
#
#         return JsonResponse({
#             'deleted': delete_item,
#             'item_added': item_added,
#             'line_total': total,
#             'subtotal': subtotal,
#             'tax_total': tax_total,
#             'cart_total': cart_total,
#             'flash_msg': flash_msg,
#             'total_items': total_items,
#         })
#
#     context = {
#         'object': self.get_object()
#     }
#     template = self.template_name
#     return render(request, template, context)

    # class admin:
    #     def bookmanage(self, request):
    #         books = models.Book.objects.all()
    #         template = loader.get_template('admin/bookmanage.html')
    #         context = {
    #                     'books': books,
    #                 }
    #         return HttpResponse(template.render(context, request))
    #
    #     def deletebook(self, request, list_of_books):
    #         if list_of_books:
    #             for id in list_of_books:
    #                 models.Book.objects.get(pk=id).delete()
    #         return HttpResponseRedirect(reverse('bookmanage'))
    #
    #     def createbook(self, request):
    #         list_of_cate = models.Category.objects.all()
    #         template = loader.get_template('admin/create.html')
    #         context = {
    #                     'list_of_cate': list_of_cate,
    #                 }
    #         return HttpResponse(template.render(context, request))
    #
    #     def addnewbook(self, request):
    #         book_info = request.POST
    #         new_one = models.Book()
    #         new_one.save()
    #         return render(request, 'addnewbook', {})
    #
    #     def updatebook(self, request, book_id):
    #         book = models.Book.objects.get(pk=book_id)
    #         current_cate = book.cate_id
    #         list_of_cate = models.Category.objects.all()
    #         template = loader.get_template('admin/update.html')
    #         context = {
    #                     'list_of_cate': list_of_cate,
    #                     'book': book,
    #                     'current_cate': current_cate,
    #                 }
    #         return HttpResponse(template.render(context, request))
