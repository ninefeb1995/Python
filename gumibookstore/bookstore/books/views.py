from books.models import *
from books.serializers import BookSerializer, UserSerializer
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.template import loader
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.exceptions import *
from django.http import *
from books.permissions import IsAdminOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    """
    This viewset auto provides `list`, `retrieve`, `create`, `update`
    and destroy actions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly)

    def perform_create(self, serializer):
        serializer.save()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset auto provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


def category(request, cate_id):
    """
    The function which shows list of books of a catagory
    :param request: request GET data from clients
    :param cate_id: ID of category needing to show
    :return: render list of books according to catagory
    """
    categories = Category.objects.all()
    books_by_cate = Book.objects.filter(categories=cate_id)
    get_cate = Category.objects.get(pk=cate_id)
    paginator = Paginator(books_by_cate, 3) #Paginator helping for paging
    current_page_number = request.GET.get('current-page')
    try:
        quantity_of_books_per_page = paginator.page(current_page_number)
    except EmptyPage:
        quantity_of_books_per_page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        quantity_of_books_per_page = paginator.page(1)  # Maybe redirect to 404 not found page
    print(quantity_of_books_per_page)
    context = {
                'categories': categories,
                'cate': get_cate,
                'quantity_of_books_per_page': quantity_of_books_per_page,
            }
    return render(request, 'category/category.html', context)


def auto_book(request):
    """
    The function which shows all of books
    :param request: request GET data from clients
    :return: render all of books automatically
    """
    categories = Category.objects.all()
    auto_books = Book.objects.all()
    paginator = Paginator(auto_books, 3) #Paginator helping for paging
    current_page_number = request.GET.get('current-page')
    try:
        quantity_of_books_per_page = paginator.page(current_page_number)
    except EmptyPage:
        quantity_of_books_per_page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        quantity_of_books_per_page = paginator.page(1)  # Maybe redirect to 404 not found page
    context = {
                'categories': categories,
                'quantity_of_books_per_page': quantity_of_books_per_page,
            }
    return render(request, 'book/auto_book.html', context)


def detail(request, book_id):
    """
    Showing detail of a book according to id of book
    :param request: request GET data from clients
    :param book_id: id of book in database
    :return: httpresponse to render view page
    """
    categories = Category.objects.all()
    template = loader.get_template("book/detail.html")
    try:
        get_book = Book.objects.get(pk=book_id)
        get_cate = get_book.categories.all()
        get_list_book_of_cate = Book.objects.filter(categories=get_cate)
    except: # in case book is not exist or getting data from database occuring problem
        raise Http404("Book is not exist...!")
    else:
        context = {
            'book': get_book,
            'list_book_of_cate': get_list_book_of_cate,
            'categories': categories,
        }
    return HttpResponse(template.render(context, request))
