from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Area, Data, RawData, AQI
from manage_devices.models import Node
from datetime import datetime
from datetime import timedelta
from django.http import JsonResponse
from api.serializers import DataSerialization, NodeSerialization
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.utils import timezone
from geopy.distance import great_circle
import logging

logger = logging.getLogger(__name__)


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
        active_node = Node.objects.filter(is_available=True)
        active_node_serialized = NodeSerialization(data=active_node, many=True)
        active_node_serialized.is_valid()
        active_node_count = active_node.count()

        area_count = Area.objects.count()

        dict_data = {
            'data': data_serialized.data,
            'node_count': node_count,
            'active_node': active_node_serialized.data,
            'active_node_count': active_node_count,
            'gateway_count': gateway_count,
            'area_count': area_count
        }
        return JsonResponse(dict_data, safe=False)


class DashBoardEventStream(LoginRequiredMixin, View):

    def eventstream(self, name_of_node):
        node_name = name_of_node.replace('+', ' ')
        last_connection = Node.objects.filter(name=node_name)[0].last_connect
        now = timezone.now()
        last_activity = now - last_connection
        if last_activity.total_seconds() > 60:
            return True
        latest_object = RawData.objects.filter(node_name=node_name).latest()
        stream = '&value=' + str(latest_object.co) + '|' + str(latest_object.nitrogen)
        yield stream
        # if latest_object:
        #     if name_of_node == 'co':
        #         # stream = 'event: co\n'
        #         # stream = 'data:' + str(latest_object.co) + '\n\n'
        #         stream = '&value=' + str(latest_object.co)
        #     else:  # type_of_data.upper() == 'oxi'
        #         # stream = 'event: oxi\n'
        #         # stream = 'data:' + str(latest_object.oxi) + '\n\n'
        #         stream = '&value=' + str(latest_object.oxi)
        #     yield stream

    @csrf_exempt
    def get(self, request, name_of_node):
        if self.eventstream(name_of_node):
            return
        response = HttpResponse(self.eventstream(name_of_node), content_type="text/event-stream")
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


class DashBoardRawData(View):

    def get(self, request):
        node_name = request.GET.get('node' or None)
        co = request.GET.get('co' or None)
        if node_name and co:
            try:
                get_node_name = Node.objects.get(name=node_name)
            except (Node.DoesNotExist, Node.MultipleObjectsReturned):
                return
            new_data = RawData(co=float(co),
                               node=get_node_name,
                               node_name=node_name,
                               measuring_date=timezone.now())
            new_data.save(force_insert=True)
            get_node_name.last_connect = timezone.now()
            get_node_name.save()
        return


class DashBoardViewAQIOnMap(View):

    def get(self, request):
        node_in_active = Node.objects.all()
        if node_in_active.count() == 0:
            return
        day = timezone.now().date() - timedelta(days=1)
        all_aqi = AQI.objects.all()
        if all_aqi.count() == 0:
            return
        aqis = all_aqi.filter(of_date=day)
        while aqis.count() == 0:
            day -= timedelta(days=1)
            aqis = AQI.objects.filter(of_date=day)
        data_to_send = {}
        for aqi in aqis:
            data_of_node = {
                'center': {
                    'lat': float(aqi.node.latitude),
                    'lng': float(aqi.node.longitude)
                },
                'aqi_value': aqi.value
            }
            data_to_send[aqi.node.name] = data_of_node
        return JsonResponse(data_to_send, safe=False)


class DashBoardViewApp(View):

    def get(self, request):
        latitude = request.GET.get('lat' or None)
        longitude = request.GET.get('long' or None)
        data_to_send = {}
        if not latitude or not longitude:
            data_to_send['status'] = 'failed'
            data_to_send['message'] = 'Location sent was error !'
            return JsonResponse(data_to_send, safe=False)
        location_app = (longitude, latitude)
        nodes = Node.objects.filter(is_available=True)
        min_in_distance = 0.0
        min_in_node = None
        total_aqi_value = 0.0
        count_aqi_value = 0
        if nodes.count() == 0:
            data_to_send['status'] = 'failed'
            data_to_send['message'] = 'There is no data in this area !'
            return JsonResponse(data_to_send, safe=False)
        for node in nodes:
            location_node = (node.longitude, node.latitude)
            distance_in_meter = great_circle(location_node, location_app).meters
            if distance_in_meter > 1600:
                continue
            if distance_in_meter < min_in_distance:
                min_in_distance = distance_in_meter
                min_in_node = node
            try:
                total_aqi_value += AQI.objects.get(node=node).value
                count_aqi_value += 1
            except AQI.DoesNotExist:
                logger.error('\n\n\nError when getting AQI from node at DashBoardViewApp')
        if min_in_distance == 0.0:
            data_to_send['status'] = 'failed'
            data_to_send['message'] = 'There is no data in this area !'
            return JsonResponse(data_to_send, safe=False)
        try:
            data_from_node = Data.objects.filter(node=min_in_node).latest(field_name='measuring_date')
        except Data.DoesNotExist:
            data_to_send['status'] = 'failed'
            data_to_send['message'] = 'There is no data in this area !'
            return JsonResponse(data_to_send, safe=False)
        aqi_to_send = total_aqi_value / count_aqi_value
        if aqi_to_send <= 50.0:
            color = 1
        elif 51.0 <= aqi_to_send <= 100.0:
            color = 2
        elif 101.0 <= aqi_to_send <= 150.0:
            color = 3
        elif 151.0 <= aqi_to_send <= 200.0:
            color = 4
        elif 201.0 <= aqi_to_send <= 300.0:
            color = 5
        else:
            color = 6
        data_to_send['status'] = 'success'
        data_to_send['data'] = {
            'CO': data_from_node.co,
            'AQI': aqi_to_send,
            'color': color,
            'trend': ''
        }
        return JsonResponse(data_to_send, safe=False)
