from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'index/$', views.ReportIndex.as_view(), name='report_index'),
    url(r'showchart/$', views.ReportShowOnView.as_view(), name='report_showchart'),
    # url(r'download/$', views.ReportExport.as_view(), name="report_download"),
]
