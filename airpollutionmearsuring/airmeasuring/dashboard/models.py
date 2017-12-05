from django.db import models
from django.utils import timezone
from manage_devices.models import Node
import schedule
import time
import logging

logger = logging.getLogger(__name__)


class RawData(models.Model):
    co = models.FloatField()
    nitrogen = models.FloatField()
    sulphur = models.FloatField()
    pmten = models.FloatField()
    ozone = models.FloatField()
    measuring_date = models.DateTimeField(auto_created=True)
    node = models.ForeignKey('manage_devices.Node', on_delete=models.SET_NULL, null=True)
    node_name = models.CharField(max_length=255)  # This field is to ensure data belonged
    # to what when node has been deleted

    class Meta:
        get_latest_by = "measuring_date"


class Data(models.Model):
    co = models.FloatField()
    nitrogen = models.FloatField()
    sulphur = models.FloatField()
    pmten = models.FloatField()
    ozone = models.FloatField()
    measuring_date = models.DateField(default=timezone.now())
    area = models.ForeignKey('Area', on_delete=models.CASCADE)
    node = models.ForeignKey('manage_devices.Node', on_delete=models.SET_NULL, null=True)


class Area(models.Model):
    name = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AQI(models.Model):
    value = models.FloatField()
    of_date = models.DateField(default=timezone.now())
    node = models.ForeignKey('manage_devices.Node', on_delete=models.SET_NULL, null=True)


def job_schedule():
    schedule.every().day.at('11:59').do(calculate_data_from_rawdata)
    while True:
        schedule.run_pending()
        time.sleep(1)


def calculate_data_from_rawdata():
    day = timezone.now().date()
    all_data = RawData.objects.filter(measuring_date=day)
    all_node = Node.objects.all()
    logger.info('\n\nCalculate data on %s\n', day.strftime('%A, %d. %B %Y %I:%M%p'))
    for node in all_node:
        all_data_by_node = all_data.filter(node=node)
        if all_data_by_node.count() <= 0:
            logger.info('\nNot add data of ', node.name)
            continue
        avg_co = 0.0
        avg_nitrogen = 0.0
        avg_sulphur = 0.0
        avg_pmten = 0.0
        avg_ozone = 0.0
        count_co = 0
        count_nitrogen = 0
        count_sulphur = 0
        count_pmten = 0
        count_ozone = 0
        aqi_co = 0.0
        aqi_nitrogen = 0.0
        aqi_sulphur = 0.0
        aqi_pmten = 0.0
        aqi_ozone = 0.0
        for data in all_data_by_node:
            if data.co:
                avg_co += data.co
                count_co += 1
            if data.nitrogen:
                avg_nitrogen += data.nitrogen
                count_nitrogen += 1
            if data.sulphur:
                avg_sulphur += data.sulphur
                count_sulphur += 1
            if data.pmten:
                avg_pmten += data.pmten
                count_pmten += 1
            if data.ozone:
                avg_ozone += data.ozone
                count_ozone += 1
        new_data = Data(measuring_date=day, node=node, area=node.area)
        if count_co != 0:
            avg_co /= count_co
            new_data.co = avg_co
            aqi_co = avg_co / 5.0 * 100
        if count_nitrogen != 0:
            avg_nitrogen /= count_nitrogen
            new_data.nitrogen = avg_nitrogen
            aqi_nitrogen = avg_nitrogen / 0.1 * 100
        if count_sulphur != 0:
            avg_sulphur /= count_sulphur
            new_data.sulphur = avg_sulphur
            aqi_sulphur = avg_sulphur / 0.3 * 100
        if count_pmten != 0:
            avg_pmten /= count_pmten
            new_data.pmten = avg_pmten
            aqi_pmten = avg_pmten / 0.005 * 100
        if count_ozone != 0:
            avg_ozone /= count_ozone
            new_data.ozone = avg_ozone
            aqi_ozone = avg_ozone / 0.06 * 100
        new_data.save(force_insert=True)
        aqi_by_day_by_node = max([aqi_co, aqi_nitrogen, aqi_sulphur, aqi_pmten, aqi_ozone])
        aqi_of_node = AQI(node=node, of_date=day, value=aqi_by_day_by_node)
        aqi_of_node.save(force_insert=True)
        logger.info('\nAdd data of ', node.name)
