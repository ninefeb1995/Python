from django.conf.urls import url, include
from dashboard import views

urlpatterns = [
    url(r'index/$', views.index, name="index"),
]
