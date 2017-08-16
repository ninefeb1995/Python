from django.conf.urls import url, include
from custom_auth import views
from django.contrib.auth import views as django_auth
from django.conf.urls.static import settings

urlpatterns = [
    url(r'login/$', django_auth.login, {'template_name': 'custom_auth/login.html'}, name="login"),
    url(r'logout/$', django_auth.logout, {'next_page': settings.LOGIN_URL}, name="logout"),


]
