"""airmeasuring URL Configuration

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
from django.conf import settings
from core import views
from dashboard.models import job_schedule
from django.utils import timezone
import threading
import logging


logger = logging.getLogger(__name__)
logger.info("\n\nServer started on %s \n\n", timezone.now().strftime('%A, %d. %B %Y %I:%M%p'))
t = threading.Thread(target=job_schedule)
t.daemon = True
t.start()

urlpatterns = [
    url(r'^', include('introduction.urls')),
    url(r'^introduction/', include('introduction.urls', namespace='introduction')),
    url(r'^authen', include('custom_auth.urls', namespace='custom_auth')),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^manage-users/', include('manage_users.urls', namespace='manage_users')),
    url(r'^manage-devices/', include('manage_devices.urls', namespace='manage_devices')),
    url(r'^report/', include('report.urls', namespace='report')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler403 = views.error403
handler404 = views.error404
handler500 = views.error500
handler400 = views.error400
