from django.conf.urls import url, include
from .views import IntroductionIndex

urlpatterns = [
    url(r'^$', IntroductionIndex.as_view(), name='index'),
]
