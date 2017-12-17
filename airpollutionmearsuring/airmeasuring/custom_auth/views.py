from random import randint
from django.contrib.auth import authenticate
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def custom_check_credentials(request):
    username = request.POST['username']
    password = request.POST['password']
    check_user = authenticate(request=request, username=username, password=password)
    if check_user:
        response = HttpResponse('successful')
    else:
        response = HttpResponse('failed')
    return response


def custom_check_email(request):
    email = request.POST['email']
    try:
        User.objects.get(email=email)
        response = HttpResponse('successful')
        code = generatesecurecode()
        html_content = render_to_string('reset_password_email.html', {'code': code})
        content = strip_tags(html_content)
        email = EmailMultiAlternatives(
           subject='Reset password - Recovery Code',
           body=content,
           from_email=settings.EMAIL_HOST_USER,
           to=[email],
           cc=[settings.EMAIL_HOST_USER]
        )
        email.attach_alternative(html_content, 'text/html')
        email.send(fail_silently=False)
    except User.DoesNotExist:
        response = HttpResponse('failed')
    return response


def generatesecurecode():
    a = str(randint(0, 9))
    b = str(randint(0, 9))
    c = str(randint(0, 9))
    d = str(randint(0, 9))
    e = str(randint(0, 9))
    f = str(randint(0, 9))
    return a + c + e + b + d + f
