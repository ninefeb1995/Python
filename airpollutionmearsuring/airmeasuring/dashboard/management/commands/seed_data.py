from random import uniform
from dashboard.models import Data, RawData, Area, AQI, calculate_data_from_rawdata
from manage_devices.models import Node
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = "Seeding initial data for database"

    def handle(self, *args, **options):
        area1 = Area(name='SUOITIEN', district='District 9', city='Ho Chi Minh', country='Viet Nam')
        area2 = Area(name='DHCNTT', district='Thu Duc District', city='Ho Chi Minh', country='Viet Nam')
        area1.save()
        area2.save()

        node1 = Node(name='Node A', area=area1, node_identification='nodea',
                     role='node_gateway', is_available=True, longitude='106.8074918', latitude='10.8679537')
        node1.save()
        node2 = Node(name='Node B', area=area1, node_identification='nodeb',
                     role='node_cell', gateway_id=node1, is_available=True,
                     longitude='106.80648565292358', latitude='10.86796223567664')
        node3 = Node(name='Node C', area=area1, node_identification='nodec',
                     role='node_cell', gateway_id=node1, is_available=True,
                     longitude='106.8070113658905', latitude='10.86717727233645')
        node2.save()
        node3.save()

        start_datetime = datetime.strptime('2017 11 01 00 00 00', '%Y %m %d %H %M %S')
        end_date = datetime.strptime('2017 11 30 23 59 59', '%Y %m %d %H %M %S')

        while start_datetime <= end_date:
            co_a = uniform(2.5, 5)
            co_b = uniform(2.5, 5)
            rawdata1 = RawData(co=co_a, measuring_date=start_datetime,
                               node=node2, node_identification=node2.node_identification)
            rawdata2 = RawData(co=co_b, measuring_date=start_datetime,
                               node=node3, node_identification=node3.node_identification)
            rawdata1.save()
            rawdata2.save()
            start_datetime += timedelta(hours=1)

        start_datetime = datetime.strptime('2017 11 01', '%Y %m %d')
        end_date = datetime.strptime('2017 11 30', '%Y %m %d')

        while start_datetime <= end_date:
            calculate_data_from_rawdata(date=start_datetime)
            start_datetime += timedelta(days=1)
