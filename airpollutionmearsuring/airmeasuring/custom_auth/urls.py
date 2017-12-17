from django.conf.urls import url, include
from django.contrib.auth import views as django_auth
from django.conf.urls.static import settings
from custom_auth.views import custom_check_credentials, custom_check_email

urlpatterns = [
    url(r'login/$', django_auth.login, {'template_name': 'custom_auth/login.html'}, name='login'),
    url(r'logout/$', django_auth.logout, {'next_page': settings.LOGIN_URL}, name='logout'),
    url(r'manual/check/user/$', custom_check_credentials, name='custom_check_user'),
    url(r'manual/check/email/$', custom_check_email, name='custom_check_email')
]
