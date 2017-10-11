from rest_framework import routers
from django.conf.urls import include, url
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserModelViewSet, base_name='manage_users')
router.register(r'datas', views.DataModelViewSet, base_name='datas')
router.register(r'rawdatas', views.RawDataModelViewSet, base_name='rawdatas')
router.register(r'nodes', views.NodeModelViewSet, base_name='nodes')
router.register(r'areas', views.AreaModelViewSet, base_name='areas')


urlpatterns = [
    url(r'^', include(router.urls)),
]