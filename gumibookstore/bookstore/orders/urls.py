from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from orders.views import OrderViewSet, api_root

# bind our ViewSet classes into a set of concrete views
order_list = OrderViewSet.as_view({
    'get': 'list'
})

order_detail = OrderViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    # url(r'^$', api_root),
    url(r'^orders/$', order_list, name='order-list'),
    url(r'^orders/(?P<pk>[0-9]+)/$', order_detail, name='order-detail'),
])
