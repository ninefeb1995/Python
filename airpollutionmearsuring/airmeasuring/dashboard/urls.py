from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'index/$', views.DashBoardView.as_view(), name="index"),
    url(r'observation/$', views.DashBoardShowOnView.as_view(), name="observation"),
    url(r'event-stream/(?P<name_of_node>[0-9a-zA-Z+]+)/$', views.DashBoardEventStream.as_view(), name="event_stream")
    # url(r'event-stream', views.event_stream, name="event_stream")
]
