from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Area, Data, RawData
from manage_devices.models import Node
from datetime import datetime
from django.http import JsonResponse
from api.serializers import DataSerialization, NodeSerialization, RawDataSerialization
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse


class DashBoardView(LoginRequiredMixin, View):
    def get(self, request):
        areas = Area.objects.all()
        return render(request, template_name='dashboard/index.html', context={
            'areas': areas,
        })


class DashBoardShowOnView(LoginRequiredMixin, View):
    def get(self, request):
        area = request.GET.get('area')
        date_start = datetime.strptime(request.GET.get('date_start'), '%a %b %d %Y %H:%M:%S %Z%z')
        date_end = datetime.strptime(request.GET.get('date_end'), '%a %b %d %Y %H:%M:%S %Z%z')
        # data = (Data.objects.filter(measuring_date__range=[date_start.date(), date_end.date()])).values('co', 'oxi')
        data = Data.objects.filter(measuring_date__range=[date_start.date(), date_end.date()], area_id=area) \
            .order_by('measuring_date')
        data_serialized = DataSerialization(data=data, many=True)
        data_serialized.is_valid()

        node_count = Node.objects.count()
        gateway_count = Node.objects.filter(role='node_gateway').count()
        active_node_count = Node.objects.filter(is_available=True).count()
        area_count = Area.objects.count()

        dict_data = {
            'data': data_serialized.data,
            'node_count': node_count,
            'active_node_count': active_node_count,
            'gateway_count': gateway_count,
            'area_count': area_count
        }

        return JsonResponse(dict_data, safe=False)


class DashBoardEventStream(LoginRequiredMixin, View):

    def eventstream(self, type_of_data):
        latest_object = RawData.objects.latest()
        if latest_object:
            if type_of_data.upper() == 'co':
                stream = 'data:' + str(latest_object.co) + '\n\n'
            else:  # type_of_data.upper() == 'oxi'
                stream = 'data:' + str(latest_object.oxi) + '\n\n'
            yield stream

    @csrf_exempt
    def get(self, request, type_of_data):
        response = HttpResponse(self.eventstream(type_of_data), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response

# @csrf_exempt
# def event_stream(request):
#     def eventStream():
#         yield "data:Server Sent Data\n\n"
#
#     response = HttpResponse(eventStream(), content_type="text/event-stream")
#     response['Cache-Control'] = 'no-cache'
#     return response
