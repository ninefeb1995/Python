"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from core import views as homeview
from rest_framework.routers import DefaultRouter
from books import views as bviews
from carts import views as cviews
from orders import views as oviews



router = DefaultRouter()  # DefaultRouter has api_root already
router.register(r'books', bviews.BookViewSet)
router.register(r'orders', oviews.OrderViewSet)
router.register(r'users', bviews.UserViewSet)


urlpatterns = [
    url(r'^$', homeview.home, name='home'),
    url(r'^home', homeview.home, name='home'),
    url(r'^category/(?P<cate_id>[0-9]+)/$', bviews.category, name='category'),
    url(r'^autobook/$', bviews.auto_book, name='autobooks'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', homeview.login, name='login'),
    url(r'^logout/$', homeview.logout, name='logout'),
    url(r'^contact/$', homeview.contact, name='contact'),
    url(r'^detail/(?P<book_id>[0-9]+)/$', bviews.detail, name='detail'),
    url(r'^my-cart/$', cviews.my_cart, name='my-cart'),
    url(r'^add-to-cart/$',cviews.add_to_cart, name='add-to-cart'),
    url(r'^remove-from-cart/$', cviews.remove_from_cart, name='remove-from-cart'),
    url(r'borrow/$', oviews.borrow, name='borrow'),
    # version can cause error??
    # url(r'api/(?P<version>(v1|v2))/', include(router.urls)),
    url(r'api/', include(router.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^api-authen/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
