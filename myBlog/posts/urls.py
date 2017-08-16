from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.post_list, name="post_list"),
    url(r'^create/$', views.post_create),
    url(r'^(?P<pk>\d+)/$', views.post_detail, name="post_detail"),
    url(r'^(?P<pk>\d+)/edit/$', views.post_update, name="post_update"),
    url(r'^(?P<pk>\d+)/delete/$', views.post_delete),
    url(r'^image/$', views.upload_image),
]


