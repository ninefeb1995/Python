from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'devices/$', views.DeviceListView.as_view(), name='device_list'),
]