from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'index/$', views.DashBoardView.as_view(), name='dashboard_index'),
    url(r'observation/$', views.DashBoardShowOnView.as_view(), name='dashboard_observation'),
    url(r'event-stream/(?P<name_of_node>[0-9a-zA-Z+]+)/$',
        views.DashBoardEventStream.as_view(), name='dashboard_event_stream'),
    # url(r'event-stream', views.event_stream, name='event_stream'),
    url(r'rawdata/', views.DashBoardRawData.as_view(), name='dashboard_rawdata'),
    url(r'aqionmap/', views.DashBoardViewAQIOnMap.as_view(), name='dashboard_aqionmap'),
    url(r'app/', views.DashBoardViewApp.as_view(), name='dashboard_app'),
]
