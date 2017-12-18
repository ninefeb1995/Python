from random import randint
from django.contrib.auth import authenticate
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import threading


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
        threading.Thread(target=send_mail, args=(code, email)).start()
        request.session['email'] = email
        request.session['requestresetpassword'] = code
        request.session.set_expiry(300)
    except User.DoesNotExist:
        response = HttpResponse('failed')
    return response


def custom_check_code(request):
    if 'requestresetpassword' in request.session:
        code_test = request.POST['code']
        code = request.session['requestresetpassword']
        if code == code_test:
            response = HttpResponse('successful')
        else:
            response = HttpResponse('failed')
    else:
        response = HttpResponse('expired')
    return response


def generatesecurecode():
    a = str(randint(0, 9))
    b = str(randint(0, 9))
    c = str(randint(0, 9))
    d = str(randint(0, 9))
    e = str(randint(0, 9))
    f = str(randint(0, 9))
    return a + c + e + b + d + f


def send_mail(code, email):
    html_content = render_to_string('reset_password_email.html', {'code': code})
    content = strip_tags(html_content)
    email_to_send = EmailMultiAlternatives(
        subject='Reset password - Recovery Code',
        body=content,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
        cc=[settings.EMAIL_HOST_USER]
    )
    email_to_send.attach_alternative(html_content, 'text/html')
    email_to_send.send(fail_silently=False)


def custom_reset_password(request):
    password = request.POST['newpassword']
    if 'email' not in request.session:
        response = HttpResponse('expired')
        return response
    email = request.session['email']
    if password and email:
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            response = HttpResponse('successful')
        except:
            response = HttpResponse('failed')
    else:
        response = HttpResponse('failed')
    return response
