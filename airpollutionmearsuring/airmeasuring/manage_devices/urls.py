from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^devices/$', views.DeviceListView.as_view(), name='device_list'),
    url(r'^devices/(?P<pk>[0-9]+)/$', views.DeviceDetailView.as_view(), name='device_detail'),
    url(r'^devices/new/$', views.DeviceNewView.as_view(), name='device_new'),
]