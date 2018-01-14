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
from time import sleep

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


lastest_id = {}


class DashBoardEventStream(LoginRequiredMixin, View):

    def eventstream(self, data):
        # node_name = name_of_node.replace('+', ' ')
        # last_connection = Node.objects.filter(node_identification=name_of_node)[0].last_connect
        # now = timezone.now()
        # last_activity = now - last_connection
        # if last_activity.total_seconds() > 60:
        #     return True
        stream = '&value=' + str(data.co) + '|' + str(data.nitrogen)
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
        # if self.eventstream(name_of_node):
        #     return
        count = 0
        while True:
            count += 1
            latest_object = RawData.objects.filter(node_identification=name_of_node).latest()
            id_of_latest = latest_object.id
            global lastest_id
            if name_of_node not in lastest_id or lastest_id[name_of_node] != id_of_latest:
                lastest_id[name_of_node] = id_of_latest
                break
            sleep(1)
            if count == 1:
                return
        response = HttpResponse(self.eventstream(latest_object), content_type='text/event-stream')
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
        node_identification = request.GET.get('node' or None)
        co = request.GET.get('co' or None)
        if node_identification and co:
            try:
                get_node_identification = Node.objects.get(node_identification=node_identification)
            except (Node.DoesNotExist, Node.MultipleObjectsReturned):
                response = HttpResponse('Error')
                return response
            new_data = RawData(co=float(co),
                               node=get_node_identification,
                               node_identification=node_identification,
                               measuring_date=timezone.now())
            new_data.save(force_insert=True)
            get_node_identification.last_connect = timezone.now()
            get_node_identification.save()
            response = HttpResponse('Success')
        else:
            response = HttpResponse('Error')
        return response


class DashBoardViewAQIOnMap(View):

    def get(self, request):
        node_in_active = Node.objects.filter(is_available=True)
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
        # min_in_distance = 0.0
        # min_in_node = None
        total_aqi_value = 0.0
        count_aqi_value = 0
        dict_distance_node = {}
        if nodes.count() == 0:
            data_to_send['status'] = 'failed'
            data_to_send['message'] = 'There is no data in this area !'
            return JsonResponse(data_to_send, safe=False)
        for index, node in enumerate(nodes):
            location_node = (node.longitude, node.latitude)
            distance_in_meter = great_circle(location_node, location_app).meters
            if distance_in_meter > 1600:
                continue
            dict_distance_node[distance_in_meter] = node
            # if index == 0 or distance_in_meter < min_in_distance:
            #     min_in_distance = distance_in_meter
            #     min_in_node = node
            try:
                total_aqi_value += AQI.objects.filter(node=node).latest(field_name='of_date').value
                count_aqi_value += 1
            except AQI.DoesNotExist:
                logger.error('\n\n\nError when getting AQI from node at DashBoardViewApp')
        if len(dict_distance_node) == 0:
            data_to_send['status'] = 'failed'
            data_to_send['message'] = 'There is no data in this area !'
            return JsonResponse(data_to_send, safe=False)
        ordered_dict = sorted(dict_distance_node.items(), key=lambda x: x[0])
        for item in ordered_dict:
            try:
                data_from_node = Data.objects.filter(node=item[1]).latest(field_name='measuring_date')
                break
            except Data.DoesNotExist:
                continue
        if not data_from_node:
            data_to_send['status'] = 'failed'
            data_to_send['message'] = 'There is no data in this area !'
            return JsonResponse(data_to_send, safe=False)
        # if min_in_distance == 0.0:
        #     data_to_send['status'] = 'failed'
        #     data_to_send['message'] = 'There is no data in this area !'
        #     return JsonResponse(data_to_send, safe=False)
        # try:
        #     data_from_node = Data.objects.filter(node=min_in_node).latest(field_name='measuring_date')
        # except Data.DoesNotExist:
        #     data_to_send['status'] = 'failed'
        #     data_to_send['message'] = 'There is no data in this area !'
        #     return JsonResponse(data_to_send, safe=False)
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
            'CO': "%.2f" % round(data_from_node.co, 2),
            'AQI': "%.2f" % round(aqi_to_send, 2),
            'color': color,
            'trend': 0
        }
        logger.info('\n\n\nApp with ip:%s getting data', get_client_ip(request))
        return JsonResponse(data_to_send, safe=False)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
