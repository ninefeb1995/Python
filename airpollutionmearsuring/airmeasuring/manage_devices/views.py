from django.shortcuts import render
from django.shortcuts import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Node
from dashboard.models import Area
from api.serializers import NodeSerialization
from django.contrib import messages
from django.http import HttpResponseRedirect


class DeviceListView(LoginRequiredMixin, View):

    def get(self, request):
        areas = Area.objects.all()
        gateways = Node.objects.filter(role='node_gateway')
        return render(request, template_name='manage_devices/index.html', context={
            'areas': areas,
            'gateways': gateways,
        })


class DeviceDetailView(LoginRequiredMixin, View):

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get("_method", '').lower()
        if method == "put":
            return self.put(*args, **kwargs)
        if method == "delete":
            return self.delete(*args, **kwargs)
        return super(NodeSerialization, self).dispatch(*args, **kwargs)

    def get(self, request, pk):
        pass

    def put(self, request, pk):
        instance = Node.objects.get(pk=pk)
        check_role_of_device = request.POST.get('iCheck')
        if check_role_of_device == 'node_gateway':
            instance.role = 'node_gateway'
        else:
            instance.role = 'node_cell'
            gateway_id = Node.objects.get(pk=request.POST.get('node_gateway_id', instance.gateway_id))
            instance.gateway_id = gateway_id
        if request.POST.get('node_location'):
            instance.is_available = True
            longitude, latitude = request.POST.get('node_location').split(';')
            instance.longitude = longitude
            instance.latitude = latitude
        instance.name = request.POST.get('node_name', instance.name)
        instance.area = Area.objects.get(pk=request.POST.get('node_area', instance.area))
        instance.node_identification = request.POST.get('node_identification', instance.node_identification)
        try:
            instance.save()
            messages.success(request, 'Updating {} is successful'.format(instance.name))
        except:
            messages.error(request, 'Updating is failed')
        return HttpResponseRedirect(reverse('manage_devices:device_list'))

    def delete(self, request, pk):
        node = Node.objects.get(pk=pk)
        node.delete()
        messages.success(request, 'Deleting {} is successful'.format(node.name))
        return HttpResponseRedirect(reverse('manage_devices:device_list'))


class DeviceNewView(LoginRequiredMixin, View):

    def post(self, request):
        check_role_of_device = request.POST.get('iCheck')
        data = {}
        if check_role_of_device == 'node_gateway':
            data['role'] = 'node_gateway'
        else:
            data['role'] = 'node_cell'
            data['gateway_id'] = Node.objects.get(pk=request.POST.get('node_gateway_id'))
        if request.POST.get('node_location'):
            data['is_available'] = True
            longitude, latitude = request.POST.get('node_location').split(';')
            data['longitude'] = longitude
            data['latitude'] = latitude
        data['name'] = request.POST.get('node_name')
        data['area'] = Area.objects.get(pk=request.POST.get('node_area'))
        data['node_identification'] = request.POST.get('node_identification')
        try:
            node = Node.objects.create(**data)
            messages.success(request, 'Creating {} is successful'.format(node.name))
        except:
            messages.error(request, 'Creating is failed')
        return HttpResponseRedirect(reverse('manage_devices:device_list'))
