from rest_framework import routers
from django.conf.urls import include, url
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserModelViewSet, base_name="manage_users")

urlpatterns = [
    url(r'^', include(router.urls)),
]