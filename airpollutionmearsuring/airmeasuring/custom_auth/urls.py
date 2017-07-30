from django.conf.urls import url, include
from custom_auth import views

urlpatterns = [
    url(r'login/$', views.login, name="login"),
]
