from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models import Area
from dashboard.models import Data
from dashboard.models import RawData
from manage_devices.models import Node
from django.http import JsonResponse
from django.http import HttpResponse
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.db.models import Avg
from django.template.loader import get_template
from django.template.loader import render_to_string
from api.serializers import DataSerialization, NodeSerialization, RawDataSerialization, AreaSerialization


class ReportIndex(LoginRequiredMixin, View):
    def get(self, request):
        areas = Area.objects.all()
        return render(request, template_name='report/index.html', context={
            'areas': areas,
        })


class ReportShowOnView(LoginRequiredMixin, View):
    def get(self, request):
        area = request.GET.get('area')
        date_start = datetime.strptime(request.GET.get('month_start'), '%a %b %d %Y %H:%M:%S %Z%z')
        date_end = datetime.strptime(request.GET.get('month_end'), '%a %b %d %Y %H:%M:%S %Z%z')

        if area == 'all':
            areas = Area.objects.all()
            areas_serialized = AreaSerialization(data=areas, many=True)
            areas_serialized.is_valid()
            data_to_send = {}
            nodes_to_send = {}
            for area in areas:
                data_by_area_and_day = Data.objects.filter(measuring_date__range=[date_start.date(), date_end.date()],
                                                           area_id=area).order_by('measuring_date')
                nodes_by_area = Node.objects.filter(area=area)
                data_by_area = {}
                for node in nodes_by_area:
                    data_by_node = data_by_area_and_day.filter(node=node)
                    data_serialized = DataSerialization(data=data_by_node, many=True)
                    data_serialized.is_valid()
                    data_by_area[node.id] = data_serialized.data
                data_to_send[area.id] = data_by_area
                nodes_serialized = NodeSerialization(data=nodes_by_area, many=True)
                nodes_serialized.is_valid()
                nodes_to_send[area.id] = nodes_serialized.data
            dict_data = {
                'data': data_to_send,
                'areas': areas_serialized.data,
                'nodes': nodes_to_send
            }
        else:
            area_object = Area.objects.get(pk=area)
            data_by_area_and_day = Data.objects.filter(measuring_date__range=[date_start.date(), date_end.date()],
                                                       area_id=area).order_by('measuring_date')
            area_serialized = AreaSerialization(instance=area_object)
            nodes = Node.objects.filter(area=area)
            data_to_send = {}
            for node in nodes:
                data_by_node = data_by_area_and_day.filter(node=node)
                data_serialized = DataSerialization(data=data_by_node, many=True)
                data_serialized.is_valid()
                data_to_send[node.id] = data_serialized.data
            nodes_serialized = NodeSerialization(data=nodes, many=True)
            nodes_serialized.is_valid()
            dict_data = {
                'data': data_to_send,
                'area': area_serialized.data,
                'nodes': nodes_serialized.data
            }
        return JsonResponse(dict_data, safe=False)


# def aveage_data_by_month(data):
#     data


# class ReportExport(LoginRequiredMixin, View):
#     def get(self, request):
#         htmp_template = get_template('report/index.html')
#         html_string = htmp_template.render()
#         pdf_file = HTML(string=html_string).write_pdf()
#         response = HttpResponse(pdf_file, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment;filename="report.pdf"'
#         return response
