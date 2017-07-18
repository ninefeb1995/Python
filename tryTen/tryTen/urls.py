from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from profiles import views as profiles_view
from contact import views as contact_view
from checkout import views as checkout_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', profiles_view.home, name='home'),
    url(r'^about/', profiles_view.about, name='about'),
    url(r'^profile/', profiles_view.userProfile, name='profile'),
    url(r'^contact/', contact_view.contact, name='contact'),
    url(r'^checkout/', checkout_view.checkout, name='checkout'),
    url(r'^accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

