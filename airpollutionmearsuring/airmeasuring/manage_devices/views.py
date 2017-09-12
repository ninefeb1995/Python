from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class DeviceListView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, template_name='manage_devices/index.html')


