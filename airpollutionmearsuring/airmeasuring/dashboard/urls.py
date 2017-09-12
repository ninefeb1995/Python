from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'index/$', views.DashBoardView.as_view(), name="index"),
    url(r'observation/$', views.DashBoardShowOnView.as_view(), name="observation"),
]
