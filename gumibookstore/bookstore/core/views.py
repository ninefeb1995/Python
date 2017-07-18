from django.shortcuts import render
from books.models import Book
from books.models import Category
from django.contrib.auth import authenticate
from django.contrib import auth
from django.template import loader
from books.models import *
from django.http import *
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    """
    Redering home page, this includes all of books
    :param request: request GET home page from users
    :return: home page redering
    """
    featured_books = Book.objects.filter(condition='old')
    new_books = Book.objects.filter(condition='new')
    categories = Category.objects.all()
    context = {
        'featured_books': featured_books,
        'new_books': new_books,
        'categories': categories,
    }
    return render(request, 'home.html', context)


def login(request):
    """
    Loading login page and handling loging in action
    :param request: request is GET or POST
            if GET, this will load logging in page, otherwise executing logging in action
    :return: rendering logging in page, administrator's page or clients' page
    """
    template = loader.get_template('authentication/login.html')
    categories = Category.objects.all()
    context = {'categories': categories, }
    if request.POST:  # When users input their username and password and press Login button
        content = request.POST
        username = content.get('username')
        password = content.get('password')
        if username and password:
            # After passing authentication
            user = authenticate(username=username, password=password)
            if not user:
                context = {
                    'validator': "**Login information is not valid",
                    'categories': categories,
                    'username': username,
                    'password': password
                }
                return HttpResponse(template.render(context, request))
            else:
                auth.login(request, user)
                if user.is_superuser:
                    pass
                    return HttpResponseRedirect('/admin')
                else:
                    return home(request)
    #else loading logging in page
    return HttpResponse(template.render(context, request))


def logout(request):
    """
    Logging out action
    :param request: GET to log out
    :return: 'next page' is the page where users press "Log out"
    """
    auth.logout(request)
    return HttpResponseRedirect(request.GET.get('next'))


def contact(request):
    """
    Handling contact request and send email to administrator
    :param request:
    :return:
    """
    content = request.POST
    template = loader.get_template('contact/contact.html')
    categories = Category.objects.all()
    context = {
        'is_sent': 'false',
        'categories': categories,
    }
    if content.get('email') is not None:
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
        context = {
            'is_sent': 'true',
            'categories': categories,
        }
    return HttpResponse(template.render(context, request))
