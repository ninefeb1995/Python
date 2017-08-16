from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.UserListView.as_view(), name='user_list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='user_detail'),
    url(r'^users/new/$', views.UserNewView.as_view(), name='user_new'),

]